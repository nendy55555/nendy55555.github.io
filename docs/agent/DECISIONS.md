# DECISIONS — thomasnendick.com

Decisions made during the Pre-Max-Downgrade Hardening Pass. The
*one-line* version of each decision lives in `adr-log.md`. The full
reasoning lives here, in the order the decisions were made.

---

## D-001 · Treat the workspace as a single project

**Date:** 2026-04-20
**Context:** The mission template framed hardening as a per-project loop
across many projects. The workspace contains exactly one project — a
static personal site — with no backend, no build step, and no runtime
Claude dependency.

**Decision:** Concentrate all hardening on the one project. Skip the
multi-project loop, the API-tier downgrade, and the cross-project
utility extraction.

**Why:** The framing existed to compress cost across many surfaces.
There is one surface. Adapting honestly is cheaper than pretending the
template applies.

---

## D-002 · Defer all but one git commit to a single terminal one-liner

**Date:** 2026-04-20
**Context:** The macOS bind-mount that exposes the workspace folder to
the sandbox has permission flags that block the sandbox from unlinking
files inside `.git/`. After the first successful commit (`1fa978b`),
stale `.git/HEAD.lock`, `.git/index.lock`, and
`.git/objects/maintenance.lock` files persisted and could not be
deleted via `rm`, `unlink`, `chmod`, or `python3 os.unlink`. All
returned `Operation not permitted`.

**Decision:** Stop attempting in-session commits. Bundle all remaining
changes into one atomic commit Thomas runs from the host terminal at
the end of the session. The exact command lives in `HARDENING-REPORT.md`.

**Why:** Burning ten minutes per attempt against a permission boundary
the sandbox cannot cross is waste. The host shell does not have the
problem. One commit at the end is also cleaner from a history-reading
standpoint than a chain of micro-commits during a single hardening pass.

---

## D-003 · Compress portrait to 1600px @ quality 82 progressive JPEG

**Date:** 2026-04-20
**Context:** `assets/leahsofiaphoto-11416.jpg` was 5.1 MB and 3571×5356
pixels. The hero portrait renders at ~200 px wide; the about-tab
portrait renders at <800 px on a 2x retina display.

**Decision:** Resize to 1600 px on the long edge, save as progressive
JPEG at quality 82. Keep the original as
`assets/.leahsofiaphoto-11416.original.jpg` (gitignored via the dotfile
pattern).

**Why:**
- **1600 px** gives 2x headroom over the largest render size without
  burning bytes for resolution no display will use.
- **Quality 82** is the inflection point on JPEG perceptual loss for
  portrait photography — under 80 you start seeing skin-tone banding;
  over 85 the file size grows faster than visible quality.
- **Progressive** lets the browser paint a low-fi preview before the
  full image arrives, which matters more than absolute byte count on
  slow connections.
- **Local original kept** because re-encoding from a re-encoded JPEG
  compounds loss. If we ever need to re-export, we go from the source.

Result: 5.1 MB → 256 KB (4.9% of original). Page weight cut by ~4.85 MB.

---

## D-004 · No service worker, no PWA shell, no WebP conversion

**Date:** 2026-04-20
**Context:** Standard "make it faster" playbook would suggest a service
worker for offline, WebP/AVIF conversion for smaller images, and a PWA
manifest for install-to-homescreen.

**Decision:** None of the above. Stay on plain JPEG, no service worker,
no manifest.

**Why:** The site is a personal index card. Total weight after the
portrait compression is under 1.5 MB and renders in well under a
second on broadband. The marginal performance win from WebP (~30%
smaller) does not justify the support-matrix complexity (Safari < 14,
older Android browsers). A service worker introduces a cache-invalidation
class of bug that costs more attention than the offline use case is
worth — nobody opens this site on a plane.

---

## D-005 · Password gate is obscurity, not security

**Date:** 2026-04-20
**Context:** Two project cards (Betting Tracker, Betting Model) sit
behind a `prompt()`-style modal. The password is a JS constant.

**Decision:** Keep the gate as-is. Do not strengthen it. Document the
threat model openly in `AUDIT.md`.

**Why:**
- The "protected" content is two links to externally-hosted dashboards
  that already have real auth on the host. The site-level gate exists
  to keep those entries off the casual menu, not to keep an attacker
  out of the data.
- Real security would need a server. The site has none. Adding one for
  this single feature is over-build.
- Pretending the gate is secure is worse than admitting it is not.
  A documented threat model lets future-Thomas decide based on the
  actual risk, not on the false sense the gate provides.

---

## D-006 · Validator is stdlib-only, runs in <100 ms, no network

**Date:** 2026-04-20
**Context:** The site needs a regression check that runs without an API
key after Max downgrades. Options ranged from full HTML5 conformance
checkers (`html5validator`, `tidy`) to nothing.

**Decision:** Build `scripts/validate.py` from Python stdlib only.
Check links, IDs, CSS class orphans, tag balance, and the asset
budget. Skip external network calls. Skip strict HTML5 conformance.

**Why:**
- **Stdlib only** means no `pip install`, no virtualenv, no version
  drift. `python3` ships with macOS.
- **Five focused checks** catch the regressions that have actually
  bitten this site (broken arch-page links, oversize images, dead
  CSS). Generic HTML5 conformance reports thousands of irrelevant
  hints.
- **Zero network** means the check runs on planes, in cafes, with
  Wi-Fi off. Predictability over completeness.
- **<100 ms** means the validator can sit inside a pre-commit hook or
  run on every save without the developer noticing.

---

## D-007 · Architecture template uses `{{TOKEN}}` placeholders, not Jinja or any template engine

**Date:** 2026-04-20
**Context:** Adding a new project means writing a new architecture
page. Without scaffolding, the next page tends to drift from the
voice and structure of the existing nine.

**Decision:** Ship `_template.html` as a literal file with `{{TOKEN}}`
strings to find-and-replace. No template engine, no script.

**Why:** A real templating engine (Jinja, Mustache) would add a
runtime dependency and a build step to a static site that has neither.
Find-and-replace in an editor is faster, more visible, and impossible
to break.

---

## D-008 · Odd-singleton centering never promotes a protected card

**Date:** 2026-04-21
**Context:** The project grid is two columns. When the active-tab card
count is odd, the final card spans the grid as a centered singleton.
With protected cards always at the bottom (per user rule), the "odd
final card" at any given count became the locked Betting Model — the
visual center of attention was a greyed-out lock.

**Decision:** Scope the centering rule with `:not(.protected)`. The
final public card centers if it ends up alone; a trailing locked card
never gets the spotlight.

**Why:** The layout rule was visually elevating exactly what the
content strategy is burying. Fixing the rule is cheaper than reordering
every card-count case.

**Reference:** `index.html` line ~1046; mobile override line ~1610.

---

## D-009 · Card fade-up cascade is first-load-only

**Date:** 2026-04-21
**Context:** Nine project cards animate in with a 0.08s stagger on
page load. The same cascade replayed on every tab switch (Active ↔
About ↔ Active), turning a smooth re-entry into a 1+ second wait for
content the user had just seen.

**Decision:** Gate the stagger CSS behind `body.first-load`. Drop the
class 1.5s after the window `load` event. Tab switches after that
point render instantly.

**Why:** Cards are first-impression flourish, not a repeat
performance. The intent of the animation is "welcome," not
"reintroduce."

**Reference:** CSS rules at `index.html` lines ~1546-1554. JS gate at
line ~2556.

---

## D-010 · Protected-card unlock uses semantic `<button>`, not `role="button"`

**Date:** 2026-04-21
**Context:** The audit flagged that locked `<article>` cards with
keyboard handlers were masquerading as buttons. The fix proposed in
Phase 1 was `role="button"` + managed tabindex. The codebase had
already refactored the pattern: the `<button class="lock-btn">` inside
the overlay is the sole unlock trigger.

**Decision:** Keep the semantic button. Skip adding ARIA roles to the
`<article>`. The existing comment in `index.html` ("semantic `<button>`
beats an `<article>` masquerading as one") captures the reasoning.

**Why:** ARIA is a fallback, not a substitute. A real button is
keyboard-accessible, screen-reader-labeled, and focusable without any
manual tabindex management.

**Reference:** Markup at `index.html` line ~2251; wire-up at line ~2724.

---

## D-011 · "Architecture" replaces "Technical Jargon" as the secondary link label

**Date:** 2026-04-21
**Context:** Every active-project card carried a secondary link
labeled "Technical Jargon" pointing to its architecture page. The copy
was self-deprecating warning label — "this will be technical, brace
yourself."

**Decision:** Rename the link to "Architecture." Updated both the
anchor text and the aria-label across all nine cards, plus the CSS
comment.

**Why:** User voice rules: "trust reader; skip hand-holding." The site
is confident elsewhere; apologizing for depth at the doorway to the
depth is tonal whiplash. "Architecture" is the honest label.

**Reference:** `index.html` lines ~2055 through ~2275.

---

## D-012 · About-tab entrance uses a CSS fade, not a JS-orchestrated reveal

**Date:** 2026-04-21
**Context:** Clicking the "About" tab snapped the panel into
existence. The Active tab had a staggered entrance; About had nothing.
Uneven polish between surfaces of the same tablist.

**Decision:** Add `animation: fadeIn 0.45s ... both` to
`#tab-about.active`. The animation retriggers each time the tab is
activated, which is the right behavior for tab re-entry.
`prefers-reduced-motion` disables it.

**Why:** CSS animations on class toggle are the simplest primitive for
this pattern — no JS orchestration, no observer, no flag. Keeps the
about-tab lifecycle declarative.

**Reference:** `index.html` lines ~491-498.

---

## D-013 · Hero copy drops em-dashes per voice rules

**Date:** 2026-04-21
**Context:** User's core writing rules explicitly call out em-dashes
as a pattern to avoid. The hero byline had a CSS-injected em-dash
prefix (`::before { content: '— '; }`), and the hero sub had one
mid-sentence.

**Decision:** Delete the `.hero-byline::before` rule entirely.
Rewrite the sub to use a period split instead of an em-dash:
"Groceries, rides, housing, sports. If it has friction, it gets an
agent."

**Why:** The rule is in the user's instructions. The em-dash was
ornament, not structure.

**Reference:** CSS at `index.html` line ~246; markup at line ~1997.

---

## D-014 · `.amp` ornament span removed from the hero headline

**Date:** 2026-04-21
**Context:** The headline was `An agent for everything<span class="amp">.</span>` — the period was styled as a 0.82em italic accent-deep glyph with vertical-align tweaks. Reads as punctuation-pretending-to-be-ornament.

**Decision:** Delete both the CSS rule and the span. Plain period now.

**Why:** The thesis already carries the weight. Ornamenting the period pulls a pixel of attention the sentence doesn't need. Less is honestly less here.

**Reference:** `index.html` line ~238 (CSS, now removed); line ~1993 (markup).

---

## D-015 · Company-wall logo strip removed from About tab

**Date:** 2026-04-21
**Context:** The About tab ended with a four-logo "Where I've built · 2016 → 2026" strip (EY, Clearsulting, Accenture, Deloitte). The same four companies lived in the experience timeline directly above with dates, roles, and context.

**Decision:** Delete the strip — CSS (41 lines), markup (17 lines), and the mobile overrides (3 lines). Keep the timeline as the single source.

**Why:** Visual redundancy. The timeline answers "where" plus "when" plus "doing what"; the wall answered only "where." Two signals of the same fact is noise, not reinforcement.

**Trade-off:** The wall communicated "worked at recognizable brands" faster than reading the timeline. Kept the logos inline in each timeline row (72×72 marks next to role titles), which preserves the glance-readability without doubling the block.

**Reference:** `index.html` — ~60 lines removed total.

---

## D-016 · `.project-number` switched from serif italic to mono

**Date:** 2026-04-21
**Context:** Each project card's meta row had `№ 01` in serif italic accent-rust paired with mono uppercase `.project-status` and mono `.tag` labels below. Two voices competing inside a single metadata row.

**Decision:** Mono all the way down: 0.7rem, text-muted, 0.12em tracking, uppercase. Matches `.project-status` and `.tag` exactly.

**Why:** "№ 01" is numeric metadata. Serif italic is reserved for body prose and display headlines elsewhere in the system. Unifying metadata voice lets the card's serif (the project name) carry the full weight of editorial treatment.

**Reference:** `index.html` line ~1058.

---

## D-017 · Action-icon stroke-width normalized to 1.6

**Date:** 2026-04-21
**Context:** Eleven inline SVGs (Architecture link chevrons, lock icons) used `stroke-width="1.8"`. Project icons use `1.6` via CSS; contact arrows use `1.6` inline; primary external-launch arrows use `2.0`. Three tiers with no clear rule.

**Decision:** Normalize all secondary icons to 1.6. Keep primary CTA arrows at 2.0 so the action hierarchy is legible: 1.6 for supporting icons, 2.0 for "click me first."

**Why:** Consistent stroke weight inside a tier reduces visual noise without flattening the hierarchy. The 1.6/2.0 split is now deliberate and documented.

**Reference:** 11 inline `stroke-width="1.8"` instances swapped to `1.6`.

---

## D-018 · Status pill + tag font-size bumped to 0.7rem

**Date:** 2026-04-21
**Context:** `.project-status` and `.tag` were 0.64rem with 0.12em tracking. At a 14-15px root, that rendered as ~10px — legible in the mockup, cramped in practice, especially on retina screens where kerning gets tight.

**Decision:** Bump both to 0.7rem (11-12px). Mobile `.tag` override bumped 0.66 → 0.68rem.

**Why:** Metadata should read as metadata, not as strain. 0.7rem is the accepted floor for mono uppercase labels with wide tracking.

**Reference:** `index.html` lines ~1064, ~1116, ~1570.

---

## D-019 · `--danger` token introduced for error signal

**Date:** 2026-04-21
**Context:** The password modal's error text used `color: #FF6D8A` inline. The rest of the palette is tokenized; this was the one hardcoded signal color.

**Decision:** Add `--danger: #FF6D8A` to `:root` in the signals group. Reference via `var(--danger)`.

**Why:** Single source of truth, and it gives future surfaces (form validation, toast errors) a ready-to-use token without inventing a new color.

**Reference:** `index.html` line ~61 (token); line ~1417 (usage).

---

## D-020 · Modal focus timeout bumped 30 → 60ms for iOS

**Date:** 2026-04-21
**Context:** `setTimeout(() => input.focus(), 30)` in `openModal()`. On iOS, the software keyboard's open animation and Safari's focus resolution race at 30ms — occasionally the focus lands but the keyboard doesn't open, or the keyboard opens on the wrong input.

**Decision:** Bump to 60ms. Still feels instant; past the iOS race window.

**Why:** 30ms was a desktop-tuned guess. 60ms is the smallest value that reliably clears the iOS animation schedule. No noticeable latency on desktop.

**Reference:** `index.html` line ~2522.

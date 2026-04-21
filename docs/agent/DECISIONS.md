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

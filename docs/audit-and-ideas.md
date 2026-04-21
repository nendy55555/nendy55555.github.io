# thomasnendick.com — Audit & Wow-Factor Ideas

**Prepared:** 2026-04-21
**Scope:** Full UI/UX audit of the live site + ideation for features that elevate it for a Deloitte-partner / FDE-hiring audience.
**Source of truth:** `index.html` @ 2,663 lines (local matches live deploy in size/structure).
**Status:** Findings only. No code changes yet — pick what to execute.

> **Line numbers below are approximate.** The file has ongoing edits (grew from 2,663 → 2,723 lines mid-audit). Each finding includes a search anchor you can grep to locate the exact line. Use `grep -n` against the quoted string to jump to the current location.

---

## 1. Executive Summary

### Top 3 things to fix (highest leverage, ship first)

1. **Realign the hero with your positioning.** The hero currently says "Agentic Army · Volume One" + "An agent for *everything*." For a Deloitte partner skimming, this reads as a consumer SaaS launch, not a senior strategist's credibility site. Your own DESIGN-BRIEF anchors on "Strategy, built." Decide which framing wins and commit. (*See Critical-01.*)
2. **Unify the dark-mode accent.** Light mode uses rust `#C2613A`; dark mode silently swaps to purple `#9B6DFF` (line 1832) and introduces a teal secondary with no light-mode parallel. That violates your own "single accent, scaled by role" system and makes a dark-mode toggle feel like a different brand. (*See Critical-02.*)
3. **Fix modal focus + error-message timing.** The password modal delays focus-to-input by 60ms (line ~2613), the first keystrokes can hit the page behind it; and the error message clears on modal open, which means it disappears before users can read it on second attempt. Two small JS tweaks. (*See High-02.*)

### Top 3 things to add (biggest positioning lift)

1. **One flagship case study** — `/case/grocery-shopper` or similar. 1,200-word write-up: problem → constraints → architecture decisions → outcome → "what I'd do differently." This is the single highest-leverage asset for the Deloitte → FDE positioning. Partners read methodology; cards only describe.
2. **A `/now` page** — updated quarterly alongside each "Volume." Currently reading, currently building, currently thinking. It keeps the site alive between redesigns and gives partners a reason to re-visit.
3. **A signature interactive demo on one card.** Pick one project that can be shown, not told (e.g., Rideshare Comp → live query with toy data; Dynasty FF → inline trade-value calculator). One live thing beats nine descriptions.

---

## 2. UI/UX Audit Findings

Grouped by severity. Every item names the element, a line reference, and a concrete fix. Line numbers are from `index.html` local; live may drift ±5 lines.

### Critical

**Critical-01 — Hero framing contradicts the positioning target.**
- **Where:** `index.html` hero block, ~lines 1938–1960. Anchor: `grep -n 'hero-headline' index.html`
- **Issue:** Current hero: "Agentic Army · Volume One" + "An agent for *everything*." + "Personal productivity agents, tackling the mundane tasks you don't want to spend your *free time* doing." This reads consumer / hobbyist / AI-launch. For the stated primary audience (Deloitte partners, FDE hiring), it undercuts credibility. DESIGN-BRIEF anchors the thesis on "Strategy, built." — none of that appears above the fold.
- **Fix:**
  - Headline → **"Strategy, *built*."** (the DESIGN-BRIEF anchor; one word of italic emphasis)
  - Byline → **"Most strategists stop at the deck. I ship."** (or the existing "Strategy is more honest when the strategist has shipped," which is your best line — currently buried in the About tab)
  - Sub → 1 specific sentence naming what's in the index: **"A working index of tools I've built to solve problems I hit first: groceries, concerts, rideshare, housing, fantasy, bets."**
  - Kicker → either retire "Agentic Army" or keep it as the collection *name* ("Works · Volume 01") without making it the thesis.
- **Why it matters:** Every other decision on the page is in service of whoever reads the first 8 seconds. Right now those 8 seconds say "side projects." They should say "builds where most of my peers specify."

**Critical-02 — Dark mode silently rebrands.**
- **Where:** dark-mode token block, ~line 1820+. Anchor: `grep -n '9B6DFF' index.html` (currently ~line 1835). Purple accent overrides the rust, and a teal secondary is introduced with no light-mode parallel.
- **Issue:** Light mode = warm rust + paper. Dark mode = cool purple + navy + teal. Same site, two different brands. Violates the "single accent" rule in your own brief, and any partner who toggles will register it as "not intentional."
- **Fix:** Shift the dark-mode accent to a warm rust tuned for dark backgrounds (e.g., `#E8944D` or `#EA9B5D` — same hue family, higher brightness). Remove the teal secondary unless you introduce a matching one in light mode.
- **Why it matters:** Your differentiation bet #4 is "single accent." The dark theme quietly voids that claim for half your visitors.

### High

**High-01 — Hero body copy is soft; rewrite for quiet confidence.**
- **Where:** Hero byline + sub (~lines 1952–1956), about-tab lede (~line 2310). Anchors: `grep -n 'hero-byline\|hero-sub\|about-tab-lede' index.html`
- **Issue:** Specific phrases that undercut tone:
  - "Vibe coder by night" (About lede) — slang, reads hobbyist
  - "Fascinated by agentic AI" (About para 1) — vague declarative; show, don't tell
  - "Stacking trainings to pair the strategic lens with real tech chops" (About para 2) — résumé-speak
  - "Don't want to spend your free time doing" (hero sub) — consumer framing
  - Honeymoon card: "so you don't have to open thirty browser tabs" — tech-complaint cliché
- **Fix:** Replacement lines in Appendix A. Core rule from your own brief — no throat-clearing, no adverbs, no "passionate." Apply it strictly.
- **Why it matters:** Your brief says "Trust reader. State, don't sell." Right now you're selling.

**High-02 — Modal: focus timing + error-clearing behavior.**
- **Where:** Password-modal JS block. Anchor: `grep -n 'PROTECTED_PASSWORD\|pwError\|openModal' index.html` (currently ~line 2548 and below).
- **Issue (a):** Focus is placed on the input after `setTimeout(..., 60ms)` (the 60ms is intentional for iOS keyboard timing, noted in AUDIT.md D-020). But if a user types immediately, the first few keystrokes land on the page behind the modal.
- **Issue (b):** `errorEl.textContent = ''` runs on `openModal()`, which means if a user submits a wrong password, sees the error, then tabs away and reopens, the error vanishes before they can act on it. The clear should trigger on user input, not on modal open.
- **Fix:**
  ```js
  // On open: focus the modal card immediately, then the input after 60ms.
  modalCard.focus();
  setTimeout(() => input.focus(), 60);
  // Clear error when user types, not on open.
  input.addEventListener('input', () => { errorEl.textContent = ''; });
  ```
- **WCAG:** 2.4.3 (Focus Order), 3.3.1 (Error Identification).

**High-03 — Ambient drift gradients contradict "monastic editorial."**
- **Where:** `.ambient` pseudos, lines 145–179; drift animations at 178–179
- **Issue:** Two radial gradients drift for 28–36s at ~85% opacity. Your brief says Rauno / Stripe Press / Monocle — none of those move. The drift reads more "SaaS ambient chill" than editorial stillness. Not broken, just off-brief. The fact you already disable it on mobile and on `hover: none` (line 1720, 1792) is a tell that you know it's expensive.
- **Fix:** Two options — (a) remove the drift entirely; keep grain + solid paper. (b) Keep it but drop opacity to 0.35 and stretch the animation to 50–60s so it reads as breathing, not floating. I'd pick (a).
- **Why it matters:** Restraint is the differentiator. Right now there's one motion decision pulling against it.

**High-04 — Spacing rhythm inside project cards is loose relative to the rest of the page.**
- **Where:** `.project-card` padding and gaps, `index.html` lines 924–1000
- **Issue:** Cards use `28px 30px 26px` padding with a 22px icon-meta gap. The rest of the page is disciplined on the 8/16/24/32/48 scale. This is the one place that isn't.
- **Fix:** Standardize to `24px 28px 24px` (or pure `24px`) and drop the icon-meta gap to 20px. Small change; cards will read tighter and more intentional at scale.

**High-05 — Card left-edge spine (`.project-card::before`, line 952) is decorative with no semantic payload.**
- **Where:** `.project-card::before`, lines 952–973
- **Issue:** A rust gradient bar animates in on hover. It's pretty, but it signals nothing about the card's state and nothing else on the page uses this pattern. For an editorial design, unmotivated ornament is a miss.
- **Fix:** Either (a) remove the spine entirely — the hover lift + subtle shadow is already enough affordance; or (b) make it semantic: rust on Live, muted on Archive, accent-deep on In-Build. Option (b) turns it into a status cue and earns its keep.

**High-06 — "Coming soon" cards offer an affordance (hover, role-like) but can't go anywhere.**
- **Where:** Project-soon elements at lines ~2144, 2169, 2194, 2225
- **Issue:** These have ARIA labels but are rendered as spans. Visitors may try to click them. The cards behave like dead ends with no explanation.
- **Fix:** Add `role="status"` (semantic hint it's non-interactive) and a visible micro-caption on hover: "Shipping Q3 2026" or similar. Better yet, link each Coming Soon card to a lightweight "what I'm building here" stub page with the planned architecture — that turns "coming soon" from friction into signal.

### Medium

**Medium-01 — Meta description and title tag are off-brand.**
- **Where:** Lines 5–12 (meta description, title)
- **Issue:** Title = "Thomas Nendick — Agentic Army, Volume 1." Description = "...personal fleet of productivity agents — tools built to replace the tasks he didn't want to keep doing." This is what appears in a Deloitte email preview or a Google result. It reads hobbyist.
- **Fix:**
  - Title → `Thomas Nendick — Strategy, Built` (or `…Strategy Manager → Forward Deployed Engineer`)
  - Description → `Thomas Nendick, Technology Strategy Manager at Deloitte. An index of strategy shipped — not drawn. Forward deployed engineering in progress.`

**Medium-02 — Hero portrait alt text is warm but off-context.**
- **Where:** Line 1963
- **Issue:** Alt = "Thomas Nendick with his partner and two dogs." That's the right level of human warmth, but the *purpose* of the image in the page is professional introduction. Screen-reader users get no signal that this is the author.
- **Fix:** `alt="Thomas Nendick, Technology Strategy Manager at Deloitte, photographed with his partner and two dogs."` Keeps warmth, adds identity.

**Medium-03 — Redundant `aria-disabled` on protected cards.**
- **Where:** `applyLockState()` in the JS, and `.locked` CSS block
- **Issue:** JS sets `card.setAttribute('aria-disabled', String(!unlocked))`. The CSS doesn't use that selector — `.locked` class already handles the visual state. Two sources of truth; either is fine, both is confusing.
- **Fix:** Drop the `aria-disabled` line OR drop the `.locked` toggle and style off `[aria-disabled="true"]`. Pick one.

**Medium-04 — Line-height on project card descriptions breaks from the body rhythm.**
- **Where:** `.project-desc`, line 1066
- **Issue:** Card descriptions inherit `line-height: 1.65` (body-text value) but sit at 0.93rem in a 2–3 line snippet. Editorial convention is tighter leading on smaller body fragments. Current setting looks airy and slightly under-designed next to the serif headlines above.
- **Fix:** Set `.project-desc { line-height: 1.5; }`. No other change.

**Medium-05 — Tab `aria-selected` count style conflates with "In Build" status.**
- **Where:** `.tab-btn[aria-selected="true"] .tab-count` uses `color: var(--accent)`
- **Issue:** Elsewhere `--accent-deep` is used for status ("In Build"). Selected tab count renders in display-only rust. Two things carry the same visual language.
- **Fix:** Use `--text` or `--text-secondary` for selected tab count and emphasize selection via weight change instead (`font-weight: 500` → `600`).

**Medium-06 — Hero byline is italic serif but hero sub is sans-with-italic-serif — tonal split.**
- **Where:** `.hero-byline` line 240, `.hero-sub` line 249
- **Issue:** Two adjacent blocks use different typefaces for emphasis. Editorial pages typically pick one lane.
- **Fix:** Pull the sub into sans-only with no serif italic (keep emphasis as weight change), OR move the sub to serif italic like the byline. Either works; mixing is the problem.

**Medium-07 — Animation tempo is inconsistent across interactions.**
- **Where:** Tab underline (0.3s), card hover (0.35s), scroll reveal (0.7s) — different easings in places
- **Issue:** On a site claiming editorial restraint, tempo should be one system. Three visibly different speeds feel unplanned.
- **Fix:** Adopt a 2-tier system:
  - Micro (hover, focus, underline): 240ms `cubic-bezier(0.2, 0.8, 0.2, 1)`
  - Reveal / section entry: 600ms same easing
  - Delete any third speed.

**Medium-08 — Dark mode accent contrast on small accent text.**
- **Where:** Dark-mode token block line ~1822
- **Issue:** `#9B6DFF` on `rgba(255,255,255,0.04)` (near-black) is ~6:1 — passes AA for body but borderline for 0.7rem mono type (mastheads, kickers, tags). Anything below ~10pt at that contrast starts fighting the grain overlay.
- **Fix:** Once Critical-02 is addressed (shift to warm dark accent), re-check. If you keep the purple, bump to `#B896FF` for small-type uses.

**Medium-09 — Contact lede leans on em-dash, which DESIGN-BRIEF explicitly avoids.**
- **Where:** `contact-lede` element, ~line 2489. Anchor: `grep -n 'Happy to trade notes' index.html`
- **Issue:** "Happy to trade notes — on tech strategy, forward deployment, or *anything I'm building*." Brief says "avoid em-dashes." Past audit pass already pruned em-dashes from the hero; this one was missed.
- **Fix:** `Happy to trade notes on tech strategy, forward deployment, or *anything I'm building*.`

### Low

**Low-01 — Icons on project cards are a Heroicons set; functional, not signature.**
- **Where:** All `.project-icon` SVGs in the card markup
- **Issue:** Generic line icons. They disappear into the card. A memorable editorial portfolio usually has one custom visual motif.
- **Fix (optional, M effort):** Replace with a set of one-color hand-drawn or wordmark-style glyphs; or drop icons entirely and let the number + title carry. See Feature-07 (custom glyph system).

**Low-02 — Skill-tag `:active` state missing.**
- **Where:** `.skill-tag:hover` styles; no `:active`
- **Fix:** `.skill-tag:active { transform: scale(0.98); }` for tactile feedback.

**Low-03 — "Stacking trainings" phrasing in About paragraph 2.**
- **Where:** Line 2253
- **Fix:** Replace with "Pairing strategy with shipped code."

**Low-04 — Footer font credit is fine but "Agentic Army · Volume 1" reinforces the hobbyist framing.**
- **Where:** Footer colophon ~line 2463
- **Fix:** `Works · Volume 01` is cleaner and matches the editorial frame without the gimmick.

**Low-05 — About-tab portrait has no `<figcaption>`.**
- **Where:** Line 2246–2247
- **Fix (optional):** Add a figcaption with location + year in mono: `Los Angeles · MMXXVI`. Turns it into a designed artifact instead of a stock image.

**Low-06 — `loading="lazy"` missing on the about-tab portrait since it's below the fold.**
- **Where:** Line 2247
- **Note:** Already present per local source — no action needed. Keeping as a confirmation.

**Low-07 — Protected-card password `'nendick'` is in plaintext JS.**
- **Where:** ~line 2548. Anchor: `grep -n 'PROTECTED_PASSWORD' index.html`
- **Note:** Documented intentional (soft gate for casual visitors). If the site is shared publicly on LinkedIn, pick a less guessable word. If a partner guesses it and sees the betting content, that's the failure mode you're protecting against.

### Responsive walk (375 / 768 / 1024 / 1440)

- **375px (iPhone):** Single-column hero, 96px portrait, CTA buttons stack full-width. Reads well. Two tiny concerns: (a) the theme toggle at `top: 14px; right: 14px` doesn't use `env(safe-area-inset-top)` — on notched phones in landscape it could collide with the dynamic island. Switch to `max(14px, env(safe-area-inset-top))`. (b) At 2.6rem the hero headline is fine; at 2.4rem below 380px it gets cramped against the kicker — consider adding `margin-top` to the h1 at that breakpoint.
- **768px (iPad portrait):** Clean single-column. Tab count + label spacing feels right. No issues.
- **1024px (iPad landscape / small laptop):** Two-column card grid kicks in. 9 cards = 4 rows with one lonely card in row 5. The `.project-card:not(.protected)` singleton-centering rule means the lonely card here would be a protected one (per your ordering rule); it stays left-aligned. That looks awkward — a single card pinned left with a big empty slot to its right. Consider centering *any* singleton at 1024px while keeping left-alignment at 1100px+.
- **1440px (desktop):** Container caps at 1100px, so you get symmetrical white margins. Everything sits as intended. No issues.

### What's already good — don't break on refactor

- Semantic landmarks (`header`, `main`, `section`, `nav`, `footer`) are all in the right place; Contact **is** inside `<main>` (verified lines 1972–2458). Disregard any suggestion that it isn't.
- Skip link, visible focus rings, roving tabindex on the tablist, `prefers-reduced-motion` gating — all well-implemented.
- WCAG AA contrast on paper background is real; the token comments (lines 50–58) are honest.
- Font strategy: preconnect + single URL + `display=swap` + full fallback chain. Correct and minimal.
- Portrait compression down from 5.1 MB to 256 KB is the single biggest perf win.
- The `first-load` stagger-gate trick (so stagger only runs once) is taste.
- The dark-theme toggle with `aria-pressed` + pre-paint theme-set script avoids FOUC.

### Performance quick-wins

| # | Action | Effort | Payoff |
|---|---|---|---|
| 1 | Convert `portrait.jpg` + `leahsofiaphoto-11416.jpg` to AVIF with JPEG fallback (`<picture>` element) | S | -40–60% image bytes on modern browsers |
| 2 | Add `fetchpriority="high"` to hero portrait (verify present) | XS | LCP improvement on slow connections |
| 3 | Drop the ambient drift on all devices (not just mobile) — removes a compositor layer | XS | Minor CPU/battery on laptops |
| 4 | Self-host the three Google fonts and subset to Latin only | M | -150–250 ms on first-paint; removes third-party origin |
| 5 | Extract architecture pages' `_shared.css` to a single file referenced by all 9 pages (already done — keep) | — | Already done |
| 6 | Add `link rel="modulepreload"` if you eventually split JS; right now not needed (inline JS is small) | — | N/A |

### Generic-AI-template smell test

Broadly the site is **not** AI-templated. Handcrafted-paper palette, Instrument Serif choice, no glass morphism, no SaaS blue, no rounded-everything. The one exception is the hero thesis ("Agentic Army · An agent for everything") — that specific phrase pattern is the AI-generation trope. Everything else reads human.

---

## 3. Feature Recommendations

Ranked by impact-for-audience / effort. Stars mark top picks — those are what I'd ship first in order.

### The short list

| Rank | Feature | Impact | Effort | Risk |
|---|---|---|---|---|
| ★ 1 | **Flagship case study (one)** — full write-up page for the strongest shipped project | High | M | Low |
| ★ 2 | **`/now` page** — quarterly-refreshed currents | High | S | Low |
| ★ 3 | **One live interactive demo on one card** — not all nine, just one | High | M | Medium (perf if not careful) |
| ★ 4 | **"How I work" short essay + SVG diagram** — strategy→code loop, visualized | High | M | Medium (easy to be precious) |
| ★ 5 | **Custom project glyph set replacing Heroicons** — single hand-made or wordmark style | Medium-High | M | Low |
| 6 | Cmd+K command palette for navigation | Medium | M | Medium (only if content justifies) |
| 7 | Quarterly shipping-metrics strip in the footer or `/metrics` page | Medium | S | Low |
| 8 | Annotated `/uses` page — tooling, models, hardware, opinions | Medium | S | Low |
| 9 | Keyboard-reachable `?` help overlay listing shortcuts | Medium | S | Low (only if shortcuts exist) |
| 10 | Testimonials from Deloitte peers (2–3 quotes, no avatars) | Medium-High | S-M | High if generic ("great guy") |
| 11 | View-source easter egg: ASCII manifest + signed-off author comment | Low-Medium | XS | Low |
| 12 | Project tagging + filter (Productivity / Discovery / ML / Sports) | Medium | M | Medium (UI complexity) |
| 13 | GitHub activity micro-feed on each card (last commit date, star count) | Medium | M | Medium (low stars can read unpopular) |
| 14 | "State of Forward-Deployed Engineering 2026" essay | High | L | High (needs real depth) |
| 15 | FDE self-assessment quiz (visitor diagnostic) | Medium-High | M-L | Medium (gimmicky if shallow) |
| 16 | AI-powered "ask about Thomas's work" chat | Medium | L | High (hallucination = brand damage) |
| 17 | Live telemetry: word count shipped this month, commits this week | Low-Medium | M | Low |
| 18 | Print-stylesheet that turns the page into an actual magazine-style PDF | Medium | S | Low (delightful, very on-brief) |

### The five I'd ship first, in order

**★ 1. One flagship case study.**
Pick the project you'd most want a partner to know about. Write ~1,200 words: problem → constraints (time, tech, business) → architecture decisions → outcome → "what I'd do differently." Link from the card via a **"Read the write-up"** CTA that replaces the current "Architecture" link. This is the single piece of content most likely to move a Deloitte partner from "neat" to "I want to put him on the client." Start with Grocery Shopper or Rideshare Comp — they're the most concrete. Reference: Stripe Press essays, Rauno Freiberg's writeups.

**★ 2. A `/now` page.**
200 words. "Currently building," "currently reading," "currently thinking about." Update quarterly with each Volume release. Link from masthead. Benchmark: `nownownow.com`, Derek Sivers. The reason this wins: partners come back if there's fresh signal. Without it, the site is a static artifact.

**★ 3. One live interactive demo.**
Not nine. One. Pick the project where a 15-second interaction is the whole pitch. Candidates:
- **Rideshare Comp** — a toy input ("Santa Monica → LAX, 7:30pm") that queries (or shows cached) Uber/Lyft comparisons inline. Nothing else on the site does this. One card that *does something* when every other card only *describes* is a gear-shift moment for a visitor.
- **Dynasty FF** — a small inline trade-value calculator (two players in, verdict out).
- **March Madness Dashboard** — an inline bracket scoring mini-module.
Put it *on the card itself*, expanding inline on click, not on a separate page. The contrast with the eight other descriptive cards is the point.

**★ 4. "How I Work" essay + scroll-driven SVG diagram.**
One page: `/how-i-work`. Essay ~500 words, structured:
1. Start from the deck, not around it.
2. Pick one question the deck can't answer.
3. Build the smallest thing that answers it.
4. Read the artifact. Update the deck.
5. Ship.
Accompany it with a simple left-to-right SVG: *strategy* → *prototype* → *artifact* → *decision*, with arrows that animate on scroll. Don't over-animate. This is the visual proof of your thesis line. Link from About.

**★ 5. Custom project glyph set.**
Replace Heroicons with eight purpose-made glyphs — ideally one-color, single-stroke, slightly editorial (think Monocle section markers). Can be commissioned cheap or built yourself in Figma in an afternoon. Signals "I designed this site," not "I picked a library."

### Feature ideas I deliberately skipped (and why)

- **Custom cursor.** Dated. Would fight the editorial tone.
- **Command palette for 5 pages.** Nothing to palette yet. Revisit at 15+ destinations.
- **AI chatbot.** One hallucinated sentence and a Deloitte partner walks. Not worth the failure mode yet.
- **Terminal-aesthetic section.** Cliché for engineers; reads tryhard for strategy managers.
- **3D hero scene.** Anti-brief. Your brand is paper, not WebGL.
- **Gradient text / iridescent anything.** Anti-brief.

---

## 4. Proposed Roadmap (if "do everything")

Three passes. Each is independently shippable; don't let later passes block earlier ones.

### Pass 1 — Positioning & polish (1 week, mostly copy + CSS)

Fix what's wrong before adding what's missing.

1. Rewrite hero + meta tags + about-tab lede + all soft project-card copy. **Critical-01, High-01, Medium-01.** (*3 hours of writing.*)
2. Unify dark-mode accent to warm-rust family, remove orphaned teal. **Critical-02.** (*45 min.*)
3. Fix modal focus + error-clearing timing. **High-02.** (*20 min.*)
4. Remove or slow the ambient drift. **High-03.** (*10 min.*)
5. Tighten card padding + card description line-height. **High-04, Medium-04.** (*20 min.*)
6. Resolve the spine-gradient decision (keep as status cue or remove). **High-05.** (*30 min.*)
7. Standardize animation tempo. **Medium-07.** (*30 min.*)
8. Drop em-dash from contact lede. **Medium-09.** (*1 min.*)
9. Responsive tweaks: safe-area for theme toggle, singleton-card centering at 1024. (*20 min.*)
10. `aria-disabled` cleanup on protected cards. **Medium-03.** (*10 min.*)

Deliverable end of Pass 1: the same site, but now it means what it claims to mean.

### Pass 2 — Content depth (2 weeks)

Add the things that turn the site from portfolio into proof.

1. Ship the `/now` page. (*2 hrs.*)
2. Rewrite the "Coming soon" cards as stub pages describing planned architecture. **High-06.** (*1 hr per card × 4.*)
3. Write the flagship case study. **Feature ★1.** (*6–10 hrs.*)
4. Write + diagram "How I Work." **Feature ★4.** (*8–12 hrs.*)
5. Custom glyph set for project cards. **Feature ★5.** (*3–4 hrs.*)

Deliverable end of Pass 2: there is now something to read, not just browse.

### Pass 3 — Interactive differentiation (2–3 weeks)

1. One live demo card. **Feature ★3.** (*12–20 hrs — depends on project picked.*)
2. Print stylesheet so the page prints as a magazine-style one-sheet PDF. (*2–3 hrs.*)
3. `/uses` page. (*1–2 hrs.*)
4. Project filter by tag at the tab bar. (*4–6 hrs.*)
5. (Optional) Testimonials once you have 2–3 real ones. (*1 hr design, however long to gather.*)

Deliverable end of Pass 3: the site that makes partners pause.

---

## 5. Open Questions

Blocking items I need your call on before Pass 1:

1. **Positioning — commit on Hero thesis.** Two viable directions:
   - **(A)** Revert to the DESIGN-BRIEF anchor: "Strategy, *built*." Hero centers on the FDE pivot; "Agentic Army" becomes just the Volume 01 collection name in the kicker.
   - **(B)** Double down on the current framing: "Agentic Army · An agent for everything." But then rewrite the About tab and contact section to match that tone, and accept that the audience target shifts toward AI-builder peers rather than Deloitte partners.
   I recommend (A) for the stated audience. Confirm direction.

2. **Dark-mode accent color.** Should I propose a specific rust-for-dark value (e.g., `#E8944D`), or do you want to sample something custom? Either way, this is a 3-line change.

3. **Which project gets the flagship case study first?** My vote: Grocery Shopper (most concrete user problem, clear "before/after" arc) or Rideshare Comp (most technically interesting). Your call.

4. **Which project gets the live interactive demo?** Rideshare Comp is the strongest candidate; Dynasty FF trade-value calc is the fastest to build. Pick one.

5. **"Agentic Army" — keep as collection name, retire entirely, or rename?** If we pick direction (A) above, I'd keep it as a *section label* ("Works · Volume 01 · Agentic Army") but pull it out of the thesis position.

6. **Custom glyph set — who draws it?** I can scaffold eight single-stroke SVGs in an hour if you want a starter set, or you can commission someone. Not blocking Pass 1.

7. **Case-study length and voice target.** Roughly 1,000–1,500 words, first-person, same voice rules as the homepage. Confirm or push back on the range.

---

## Appendix A — Copy rewrites at a glance

| Block | Current | Proposed |
|---|---|---|
| Block | Current | Proposed |
|---|---|---|
| Hero headline | An agent for *everything*. | Strategy, *built*. |
| Hero byline | If it's annoying enough to do twice, it may be worth building once. | Most strategists stop at the deck. I ship. |
| Hero sub | Personal productivity agents, tackling the mundane tasks you don't want to spend your *free time* doing. | An index of tools I built to solve problems I hit first — groceries, concerts, rideshare, housing, fantasy, bets. |
| Meta title | Thomas Nendick — Agentic Army, Volume 1 | Thomas Nendick — Strategy, Built |
| Meta description | Agentic Army, Volume One. Thomas Nendick's personal fleet of productivity agents — tools built to replace the tasks he didn't want to keep doing. | Thomas Nendick, Technology Strategy Manager at Deloitte. An index of strategy shipped — not drawn. Forward deployed engineering, in progress. |
| About lede | Data, AI & tech strategy by day. Vibe coder by night. Aspiring *FDE*. | Data, AI, and tech strategy by day. Builder by night. Aspiring *FDE*. |
| About para 1 | I'm a data, AI and tech strategy consultant fascinated by agentic AI. I started vibe coding products and apps to boost my personal productivity and learn while doing it. | I advise teams on data, AI, and tech strategy. My focus: how agentic systems change operating models. I build products to test those ideas — each one starts as a real problem. |
| About para 2 | I've been stacking trainings to pair the strategic lens with real tech chops. The goal: operate as a forward deployed engineer — someone who makes ideas real, not just specs them. | I'm pairing strategy with shipped code. The target: forward deployed engineer — someone who makes the idea real, not just specified. |
| Contact lede | Happy to trade notes — on tech strategy, forward deployment, or *anything I'm building*. | Happy to trade notes on tech strategy, forward deployment, or *anything I'm building*. |
| Footer colophon | Agentic Army · Volume 1 | Works · Volume 01 |

Card-level rewrites (if direction (A) is chosen):

- **Grocery Shopper:** *Pulls pricing and inventory from local stores, returns one list. One pass instead of three tabs.*
- **Concert Tracker:** *Reads my Spotify history, pulls live event APIs, surfaces only shows I'd actually go to.*
- **Dynasty FF:** *Evaluates trades against long-term value curves. Data-first roster building for year-over-year leagues.*
- **Housing Finder:** *Crawls listing APIs. Filters to my criteria, flags underpriced comps. No more tab graveyard.*
- **Honeymoon Bot:** *Handles itinerary generation across flights, stays, activities, and budget. One endpoint instead of ten.*

---

*End of report. No code changes have been made. Flag which items to execute and in what order.*

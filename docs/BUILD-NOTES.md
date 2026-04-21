# Build Notes — thomasnendick.com v1

**Date:** April 2026
**Deliverable:** `/index.html` (single file, 1,758 lines, no build step)

## What shipped

A single-file editorial portfolio. Paper canvas, serif-led hierarchy, one rust accent used only where it earns attention. Preserves the "Things I've Built" project-index DNA of the original site and wraps identity around it: hero, about, contact, footer.

**Section order:** masthead -> hero -> about -> index of works -> contact -> footer.

## Key decisions

**Thesis-first hero, name as byline.** The H1 is "Strategy, *built*." — Thomas appears as a serif italic byline beneath. Reads as a cover, not a resume. Name-as-H1 would have dragged the whole page toward LinkedIn energy.

**Portrait placeholder as designed artifact.** TN monogram in a paper-recessed frame with "Fig. 01" / "MMXXVI" corner labels. Reads as intentional, not as a missing asset. Swap for headshot when ready.

**One accent, scaled by role.**
- `--accent #C2613A` — display sizes only (passes AA-large 3:1)
- `--accent-deep #8B3F21` — body emphasis (AA 6.3:1)
- `--accent-ink #7A361B` — dense small type (AA 7.4:1)

**Work index preserved.** 8 active + 1 archive project cards, password-protected betting cards (password: `nendick`). Tab bar is ARIA-compliant with arrow keys and roving tabindex.

## Audit & fixes applied (v1 -> v1.1)

| Finding | Fix |
|---|---|
| `--text-muted #8A8075` failed AA on paper (~3.2:1) | Darkened to `#6E6459` (AA 4.99:1) |
| `.hero-sub em` using `--text` — thesis emphasis wasted | Swapped to `--accent-deep` so "I build" carries visual weight |
| `.project-status.wip` used `--accent` — failed AA at 10px | Swapped to `--accent-deep` (AA 6.3:1) |
| `.sr-only` class referenced but undefined — pw modal label visible | Added proper visually-hidden utility |
| `.hero-kicker aria-hidden="true"` hid real content from SR | Removed — kicker is now readable; rule stays `aria-hidden` |
| `role="contentinfo"` on masthead — that role belongs to the footer | Removed |
| `.contact-label { display: none }` at 420px — hidden from SR | Swapped to visually-hidden (labels still read aloud) |
| Protected card tabindex=0 always-on — duplicate focus when unlocked | `applyLockState()` removes tabindex on unlock |
| Reveal elements without GPU hint | Added `will-change: opacity, transform` during transition |
| Tablist missing direct `aria-label` | Added "Filter projects" |

## Accessibility commitments met

- WCAG 2.1 AA color contrast across all text (verified)
- Skip-to-content link, visible focus rings (`focus-visible`), logical tab order
- Semantic landmarks: `header`, `main`, `section`, `nav`, `footer`
- ARIA: tabpanels, tablist, live region on clock, `aria-modal` on password modal
- Keyboard support: arrow keys between tabs, Enter/Space opens locked cards, Escape closes modal, focus restoration on modal close
- `prefers-reduced-motion` disables ambient animation and entrance transitions
- Decorative SVGs carry `aria-hidden="true"`; functional links carry `aria-label` where needed

## Responsive

| Breakpoint | Behavior |
|---|---|
| >= 1100px | Two-col hero, two-col projects, two-col about/contact |
| 900-1099px | Same columns, tightened padding |
| 720-899px | Single-col hero/about/contact; portrait caps at 320px |
| 420-719px | Masthead wraps; type scale compresses; projects single-col |
| <420px | Headline 2.6-3.4rem; contact labels visually-hidden (SR-readable) |

## Open items (user to fill)

1. **Headshot** — replace TN monogram portrait. Drop a 4:5 image into the `.portrait` element, swap monogram for `<img>`.
2. **LinkedIn URL** — currently points to `linkedin.com/in/thomasnendick`; verify handle.
3. **Housing Finder URL** — currently `href="#"` (WIP).
4. **Concert Finder URL** — currently `href="#"` (WIP).
5. **Betting project URLs** — currently `href="#"` on the two protected cards.
6. **Password strength** — `nendick` is known to me. If site ships publicly, choose something less guessable.

## Files

- `/index.html` — single-file site, 1,758 lines
- `/docs/DESIGN-BRIEF.md` — direction, system, voice, benchmarks
- `/docs/BUILD-NOTES.md` — this file

## How to ship

Static file, no build. Serve any of:

- **GitHub Pages** — push to `gh-pages` or set `/docs` as source
- **Netlify / Vercel** — drag-drop deploy, or connect repo, set publish dir to repo root
- **Cloudflare Pages** — same pattern
- **Local preview** — `python3 -m http.server` in project root, then `http://localhost:8000`

## Voice anchors (preserved across future edits)

- "Strategy, built."
- "Most people in my practice stop at the deck — I build."
- "Strategy is more honest when the strategist has shipped."

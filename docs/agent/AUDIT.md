# AUDIT — thomasnendick.com

**Generated:** 2026-04-20 (hardening)
**Updated:** 2026-04-21 (design-audit pass — Phases 1–3)
**Pass:** Pre-Max-Downgrade Hardening + Design-Audit Refinement

## 2026-04-21 — Design-audit pass summary

Seven visual/behavioral fixes landed on top of the hardening baseline.
Every change ships in `index.html`; validator still returns PASS with
zero issues across 50 links, 15 ids, 7 classes, 562 tags, 13 assets.

| Phase | Change | Reference |
|-------|--------|-----------|
| 1.1 | Odd-singleton card centering scoped to `:not(.protected)` | D-008 |
| 1.2 | Card stagger gated to first-load only | D-009 |
| 1.3 | `color-scheme` meta set to `light dark` (dual-theme supported) | — |
| 1.4 | Protected unlock stays on semantic `<button>`, role-button skipped | D-010 |
| 1.5 | Em-dashes pruned from hero byline + sub | D-013 |
| 2.1 | `.amp` ornament span removed; plain period in headline | D-014 |
| 2.2 | Company-wall logo strip removed from About tab | D-015 |
| 2.3 | `.project-number` serif italic → mono for metadata consistency | D-016 |
| 2.4 | Inline action-icon stroke-width normalized 1.8 → 1.6 | D-017 |
| 2.7 | Status + tag font-size bumped 0.64 → 0.7rem | D-018 |
| 3.3 | Modal error color extracted to `--danger` token | D-019 |
| 3.4 | Modal focus timeout bumped 30 → 60ms for iOS | D-020 |
| 3.5 | About-tab entrance fades in on activation | D-012 |
| 3.7 | "Technical Jargon" → "Architecture" across all 9 cards + CSS comment | D-011 |

Skipped intentionally: tag separator (already clean), icon desaturation
(would drop the signature rust-accent across the grid), hero
padding-bottom (24px bottom + 48px next-section top = 72px rhythm, not
loose).

Orphans noted: removing the company wall left four horizontal SVG
logos (`ey.svg`, `accenture.svg`, `clearsulting.svg`, `deloitte.svg`)
plus assorted `*-mark.svg` and `usc.*` files unreferenced in
`assets/logos/`. Not deleted — low-cost disk footprint, may be useful
later. Clean up on a future asset pass.

---

The site is one static HTML file plus a small set of architecture pages and
assets. There is no backend, no build step, and no runtime Claude
dependency. The audit below covers what could silently break, what is
load-bearing, and where the site sits today against the exit gates.

---

## What's here

| Layer | Counts | Notes |
|-------|--------|-------|
| HTML files | 10 | `index.html` + 9 architecture pages |
| Lines in `index.html` | ~2,650 | After the dead-code pass; was 2,820 |
| Inline CSS | ~1,650 lines | All scoped inside `<style>` in `index.html` |
| Inline JS | ~150 lines | Tab roving, scroll reveal, password gate |
| Architecture pages | 9 | One per project card, share `_shared.css` |
| Assets | 13 files, 1.27 MB total | After portrait compression |
| Largest asset | 256 KB (`leahsofiaphoto-11416.jpg`) | Was 5.1 MB |
| External dependencies | 1 family of CDN fetches | Google Fonts |
| Tests | 1 | `scripts/validate.py` (offline, ~25 ms) |

---

## Runtime Claude dependency audit

| Surface | Calls Claude? | Tier | Disposition |
|---------|---------------|------|-------------|
| Index page render | No | — | No change |
| Architecture pages | No | — | No change |
| Build/deploy | No | — | No change |
| Password gate | No | — | No change |
| Validator script | No | — | No change |

Zero runtime calls. The Opus → Sonnet → Haiku downgrade framing does not
apply. The hardening value sat elsewhere and that is where this pass put
it: dead-code removal, asset budget enforcement, link integrity, docs
that match reality.

---

## External dependencies — pinned and documented

### Google Fonts

Fetched once via a single `<link>` in every HTML head:

```
https://fonts.googleapis.com/css2?
  family=Instrument+Serif:ital@0;1
  &family=DM+Sans:ital,opsz,wght@0,9..40,300..700;1,9..40,300..700
  &family=JetBrains+Mono:wght@400;500
  &display=swap
```

The URL pins specific axis ranges (italic 0..1, optical size 9..40,
weight 300..700). `display=swap` prevents flash-of-invisible-text — the
browser shows fallback fonts immediately and swaps when the web font
arrives.

Fallback chain in CSS tokens (`index.html` lines 51–53):

| Token | Web font | Fallback chain |
|-------|----------|----------------|
| `--serif` | Instrument Serif | Georgia, serif |
| `--sans` | DM Sans | system-ui, -apple-system, Segoe UI, sans-serif |
| `--mono` | JetBrains Mono | ui-monospace, SFMono-Regular, monospace |

If `fonts.googleapis.com` goes down, the site renders in Georgia + the
host system font. Visual degrade, not a site-down event.

### Project hosts (external links, not runtime deps)

| Card | Host | URL |
|------|------|-----|
| Grocery Shopper | Fly.io | thomass-cookbook.fly.dev |
| Rideshare Comp | Fly.io | rideshare-comps.fly.dev |
| Dynasty FF | GitHub Pages | nendy55555.github.io/DynastyFF |
| LA Concert Tracker | GitHub Pages | nendy55555.github.io/la-concert-tracker |
| March Madness 2026 | GitHub Pages | nendy55555.github.io/MMD-2026 |

Hard-coded in `index.html`. If a host moves or the repo is renamed, the
card link 404s. The validator does not check external URLs (zero-network
by design); a quarterly manual click-through is the mitigation.

---

## Password gate — threat model

The constant lives in plaintext JS:

```javascript
const PROTECTED_PASSWORD = 'nendick';
```

| Attack | Possible? | Why |
|--------|-----------|-----|
| Casual visitor sees protected card content | No | Card is hidden until the password is entered |
| Anyone with View Source reads the password | Yes | The constant is in the rendered HTML |
| Anyone with DevTools clears the gate | Yes | `sessionStorage.removeItem('protected-unlocked')` and re-set |
| Search engine indexes protected content | No | The protected pages are external links; the index just gates which links surface |

The gate is a **soft lock for casual visitors**, not a security boundary.
This is intentional — the protected projects (Betting Tracker, Betting
Model) are personal-finance dashboards that should not be on the menu by
default, but the actual data behind them sits behind real auth on the
hosting service.

If a future protected card needs real protection, do not strengthen the
client-side gate. Move the gate to a server (Cloudflare Access, a tiny
Worker with a shared-secret check, or a real auth provider).

See `docs/agent/DECISIONS.md` for the full reasoning.

---

## Dead code removed in this pass

| Group | Lines | Reason |
|-------|-------|--------|
| `.masthead*`, `.live-indicator`, `.live-dot`, `@keyframes pulse` | ~44 | Old top editorial masthead removed in Agentic Army rework |
| `.about-grid`, `.about-wrap`, `.about-lede`, `.about-body`, `.portrait*`, `.portrait-monogram` | ~90 | Replaced by `.about-tab-portrait` block |
| `.hero-bio-meta` | 11 | Element removed when hero bio was simplified |
| `.exp-logo .fallback`, `.edu-logo .fallback`, `.wall-fallback` | 18 | Markup uses `<img>` with no fallback span |
| Media-query remnants for the above selectors | ~25 | Orphaned by the deletions above |
| Stale comment blocks describing pruned CSS | ~10 | Replaced with two-line headers |

Total: ~200 lines of dead CSS removed. File shrank from 2,820 → ~2,650 lines.

The validator's class-orphan check now reports zero defined-but-unused
classes (excluding the JS-toggled allowlist: `is-visible`, `locked`,
`open`, `active`).

---

## Asset budget

Hard ceiling: **1 MB per asset**. Enforced by `scripts/validate.py`
asset check. Soft target: 300 KB for hero/portrait images.

| Asset | Size | Status |
|-------|------|--------|
| `leahsofiaphoto-11416.jpg` | 256 KB | Compressed from 5.1 MB |
| `portrait.jpg` | 252 KB | OK |
| `headshot.jpg` | 24 KB | OK |
| All 8 logo SVGs | <12 KB each | OK |
| `.leahsofiaphoto-11416.original.jpg` | 5.1 MB | Local-only, gitignored |

---

## Stale docs cleared

`BUILD-NOTES.md` and `DESIGN-BRIEF.md` describe the old paper/rust
"Editorial" aesthetic. The current site is dark navy + iridescent
violet ("Deep Space Glass"). They are flagged for rewrite in the
Hardening Report, not in this pass — they are reference history, not
operational. The RUNBOOK supersedes them for day-to-day editing.

---

## Exit-gate scorecard

| Gate | Status | Notes |
|------|--------|-------|
| Dead code removed | ✅ | ~200 lines, validator confirms |
| Dependencies pinned (or documented) | ✅ | Google Fonts URL pinned, fallbacks present |
| Tests exist and pass without Claude API | ✅ | `validate.py` runs in 25 ms, exit 0 |
| Every avoidable Claude call eliminated | N/A | Zero runtime calls to start |
| Remaining Claude calls on cheapest passing tier | N/A | Same |
| AUDIT.md, RUNBOOK.md, DECISIONS.md updated | ✅ | This pass |
| Git commits atomic, messages explain *why* | ⚠️ | Deferred to terminal one-liner — see HARDENING-REPORT.md |

---

## What's intentionally NOT in this pass

- **No new features.** Hardening only.
- **No design changes.** The Deep Space Glass palette is current.
- **No external link audits.** Click-through is a manual quarterly task.
- **No image-format conversion to WebP/AVIF.** JPEG at 256 KB is under
  budget; the gain isn't worth the support-matrix complexity for a
  personal site.
- **No service worker / offline mode.** The static site is small enough
  that the browser cache covers re-visits adequately.

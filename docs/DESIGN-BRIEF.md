# Design Brief — thomasnendick.com (working title)

**Date:** April 2026
**Author:** Rebuild session

## One-line direction
Editorial-quiet confidence. A serialized publication, not a landing page.

## Positioning
Thomas Nendick — Technology Strategy Manager at Deloitte, aspiring Forward Deployed Engineer. The site exists to close the distance between strategy and code. Thesis line: **"Strategy, built."**

## Audience
1. Deloitte colleagues and partners (primary) — need to see credibility, senior tone, tech fluency
2. Select clients and peers (secondary) — need to see that this person is *different* from the strategists they've met
3. Hiring or collaboration signals for future FDE-adjacent opportunities

## Aesthetic direction
"Monastic editorial." A first-issue quarterly. Warm paper canvas, single sharp accent, typographic hierarchy carrying the room. Nothing loud. Everything intentional.

## Benchmarks
- Rauno Freiberg — restraint, mono labels, quiet typography
- Stripe Press — editorial anchor, confident serif, trust through reduction
- Linear — typographic discipline, monochrome restraint
- Monocle / late-era Kinfolk — magazine-as-website

## Anti-benchmarks (avoid)
- Consultant-LinkedIn-printed-on-a-webpage
- Generic SaaS blue, gradient hero backgrounds, glass morphism
- Rounded-everything startup template
- Emoji-heavy copy, hustle energy, "I'm passionate about..."
- Over-animated microinteractions

## System

### Palette
| Token | Value | Role |
|-------|-------|------|
| `--bg` | `#F3ECE0` | Paper canvas |
| `--bg-deep` | `#EBE2D3` | Recessed surfaces (portrait frame) |
| `--bg-card` | `#FBF7EF` | Raised surfaces (cards) |
| `--bg-card-hover` | `#FFFBF3` | Card hover |
| `--text` | `#1E1A16` | Primary ink |
| `--text-secondary` | `#6A615A` | 70% ink |
| `--text-muted` | `#A49B90` | Metadata |
| `--accent` | `#C2613A` | Rust (single accent; sparingly) |
| `--accent-deep` | `#8B3F21` | Pressed states |
| `--live` | `#4A7C59` | Live/shipped indicator |
| `--rule` | `#D9CFC1` | Rule lines |

### Typography (preserved)
- **Display:** Instrument Serif — hero headlines, section ledes, project names
- **Body/UI:** DM Sans — paragraphs, labels, buttons
- **Metadata:** JetBrains Mono — mastheads, tags, kickers, numerals

Scale anchors:
- Hero headline: `clamp(3rem, 9vw, 6.8rem)`, tracking `-0.025em`, line-height `0.95`
- Section label (mono): `0.72rem`, tracking `0.18em`, uppercase
- Body: `1rem / 1.65`

### Motion
- Ambient gradient drift (28s / 36s alternating)
- Grain overlay (SVG fractalNoise, 4.5% opacity)
- Fade-up on load, staggered 80ms per card
- IntersectionObserver reveals for About and Contact
- All motion gated by `prefers-reduced-motion`

### Spacing
8 / 16 / 24 / 32 / 48 / 64 / 96 / 128. Max container: `1100px`. Section rhythm: 96–128px.

## Information architecture
1. **Masthead** — live indicator · volume · date · clock
2. **Hero** — kicker · thesis headline · byline · body · dual CTA · colophon
3. **About** — portrait frame · lede · 2 paragraphs of bio
4. **Index of Works** — tabs (Active / Archive) · project cards
5. **Contact** — lede · email / LinkedIn / GitHub
6. **Footer** — copyright · signature · colophon credit

## Voice
- First-person, quiet, specific
- No throat-clearing, no adverbs, no "passionate"
- Trust-reader. State, don't sell.
- Anchored lines: "Strategy, built." / "I build what most strategists only draw." / "Strategy is more honest when the strategist has shipped."

## Differentiation bets
1. **Editorial framing** — "Volume 01", "Index of Works", "Colophon", Roman numeral dates
2. **Typographic discipline** — tight mono kickers paired with wide serif display
3. **Intentional placeholder** — portrait frame reads as a designed artifact, not a missing asset
4. **Single accent** — rust appears only on live signals, italic emphasis, and primary CTA — not decoration

## Accessibility commitments
- Semantic landmarks (`main`, `header`, `nav`, `section`, `footer`)
- Skip-to-content link
- Visible focus ring (3px accent-wash glow) on every interactive element
- All links and buttons keyboard-reachable with logical tab order
- Color contrast ≥ 4.5:1 for body, ≥ 3:1 for large text
- `prefers-reduced-motion` disables ambient animation and entrance transitions
- `aria-hidden` on decorative SVGs; `aria-label` on the password modal

## Responsive plan
| Breakpoint | Behavior |
|------------|----------|
| ≥ 1100px | Two-column hero, two-column projects, two-column about |
| 860–1099px | Same columns, tightened padding |
| 600–859px | Single-column hero and about; single-column projects |
| < 600px | Masthead wraps; type scale compresses; colophon collapses to 2×2 grid |

## Open items for Thomas to fill in later
- Headshot (currently TN monogram placeholder)
- LinkedIn URL (placeholder assumes `linkedin.com/in/thomasnendick` — swap to actual)
- Housing Finder and Concert Finder project URLs when live
- Optional: swap rust accent to any single accent if the brand evolves

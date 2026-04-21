# Hardening Inventory — thomasnendick.com

**Generated:** 2026-04-20
**Scope:** The entire workspace is one project — a single-file static site. There is no multi-project tree, no build pipeline, no backend, and no runtime Claude dependency.

## Workspace queue (priority order)

| # | Project | Path | What it does | Claude runtime | Tests | Deps pinned | Last change | Priority |
|---|---------|------|--------------|----------------|-------|-------------|-------------|----------|
| 1 | thomasnendick.com | `/` | Personal site that indexes every tool Thomas has shipped and links to architecture write-ups. | **None** (fully static) | None | N/A (no deps) | uncommitted rework in working tree | 5/5 |

There is exactly one project. All hardening work concentrates here.

## Site map

```
/
├── index.html              # 2,820 lines. Single-file site (HTML + inlined CSS + inlined JS).
├── assets/
│   ├── headshot.jpg        # 24 KB   — used at about section
│   ├── portrait.jpg        # 252 KB  — used at hero-bio (right of hero)
│   ├── leahsofiaphoto-11416.jpg  # 5.1 MB — used at about portrait. NEEDS RESIZE.
│   └── logos/              # 8 SVGs for EY / Accenture / Deloitte / Clearsulting / USC
├── docs/
│   ├── BUILD-NOTES.md      # STALE — describes old paper/rust theme, not current dark-navy build
│   ├── DESIGN-BRIEF.md     # STALE — same
│   └── architecture/
│       ├── _shared.css
│       ├── betting-model.html
│       ├── betting-tracker.html
│       ├── concert-finder.html
│       ├── dynasty-fantasy-football.html
│       ├── grocery-shopper.html
│       ├── housing-finder.html
│       ├── march-madness-dashboard.html
│       ├── rideshare-comp.html
│       └── honeymoon-bot.html      # MISSING — referenced from index.html, 404 on click
└── .DS_Store               # committed by mistake; should be gitignored
```

No `.gitignore`, no `README`, no tests, no CI.

## Project cards (live content)

| № | Name | Status | URL | Arch doc | Notes |
|---|------|--------|-----|----------|-------|
| 01 | Grocery Shopper Assistant | Live | thomass-cookbook.fly.dev | grocery-shopper.html | |
| 02 | Rideshare Comp | Live | rideshare-comps.fly.dev | rideshare-comp.html | |
| 03 | Dynasty Fantasy Football | Live | nendy55555.github.io/DynastyFF | dynasty-fantasy-football.html | |
| 04 | LA Concert Tracker | Live | nendy55555.github.io/la-concert-tracker | concert-finder.html | filename mismatch is intentional-ish; leaving alone |
| 05 | March Madness Dashboard 2026 | Archived (kept in Active tab) | nendy55555.github.io/MMD-2026 | march-madness-dashboard.html | |
| 06 | Housing Finder | In Build | — | housing-finder.html | |
| 07 | Honeymoon Bot | In Build | — | honeymoon-bot.html | **file missing** |
| 08 | Betting Tracker | Private (gated) | — | betting-tracker.html | |
| 09 | Betting Model | Private (gated) | — | betting-model.html | |

Protected cards sit at the bottom and hold the highest № values — confirmed intentional.

## Runtime Claude dependency audit

| Surface | Claude call? | Tier | Disposition |
|---------|-------------|------|-------------|
| index.html | None | — | No change — site is static HTML/CSS/JS only. |
| architecture pages | None | — | No change. |
| build/deploy | None | — | No change. |

There is **nothing to downgrade**. The mission's "Opus→Sonnet→Haiku" framing doesn't apply to this workspace. The hardening value is elsewhere: link integrity, asset budget, maintainability without Claude, docs that match reality.

## Implicit assumptions that could silently break

1. **Google Fonts CDN stays up.** Three families (`Instrument Serif`, `DM Sans`, `JetBrains Mono`) fetched via `fonts.googleapis.com`. Fallbacks (`Georgia`, `system-ui`, `ui-monospace`) exist in tokens — visually degraded but readable if Fonts dies.
2. **Fly.io and GitHub Pages URLs.** Four external project URLs hard-coded. If Thomas re-hosts, the links silently 404.
3. **Portrait assets.** `assets/leahsofiaphoto-11416.jpg` is 5.1 MB. Any slow connection will stall page load. Needs resize.
4. **Protected password** lives in plaintext JS (`const PROTECTED_PASSWORD = 'nendick'`). Anyone with View Source can read it. Treat as obscurity, not security.
5. **Viewport quirks on iOS.** Safe-area insets and 16px input font-size are already patched — confirm they stay patched on future edits.
6. **Stale docs.** `BUILD-NOTES.md` and `DESIGN-BRIEF.md` describe the old paper/rust aesthetic. The current site is dark navy + violet. Needs rewrite.
7. **Architecture page orphans.** If a project card is removed from `index.html`, the corresponding `docs/architecture/*.html` becomes dead weight. No enforcement.
8. **Duplicate `project-status` wording.** "Archived" on March Madness is the old Archive-tab language; the tab was removed but the label survives. Intentional per Thomas — it's a post-tournament state marker, not a tab reference.

## Hardening priority — single queue

All work below targets the one project. Execution order:

1. Commit the in-flight "Agentic Army / Deep Space" rework cleanly.
2. Add `.gitignore` and remove `.DS_Store` from tracking.
3. Create the missing `honeymoon-bot.html`.
4. Compress `leahsofiaphoto-11416.jpg` from 5.1 MB → ~300 KB and re-point the `<img>`.
5. Orphan-class / dead-code sweep of `index.html`.
6. Build `scripts/validate.py` (offline link + asset + ID + CSS-orphan + tag-balance checker).
7. Refresh `BUILD-NOTES.md` and `DESIGN-BRIEF.md` to describe the current build.
8. Extract `docs/architecture/_template.html`.
9. Strengthen (or document) the password gate.
10. Write `docs/agent/RUNBOOK.md`, `AUDIT.md`, `DECISIONS.md`, `adr-log.md`.
11. Write `docs/agent/HARDENING-REPORT.md` as the exit artifact.

## Exit-gate template (applied per project, scored at end)

- [ ] Dead code removed
- [ ] Dependencies pinned (or documented as externally versioned)
- [ ] Tests exist and pass without Claude API
- [ ] Every avoidable Claude call eliminated (N/A — zero to start)
- [ ] Remaining Claude calls run on the cheapest tier that passes eval (N/A)
- [ ] AUDIT.md, RUNBOOK.md, DECISIONS.md updated
- [ ] Git commits atomic, messages explain *why*

Final scores and blockers land in `HARDENING-REPORT.md`.

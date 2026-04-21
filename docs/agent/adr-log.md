# ADR Log — thomasnendick.com

One-line summaries. Full reasoning in `DECISIONS.md`.

| ID | Date | Decision | Status |
|----|------|----------|--------|
| D-001 | 2026-04-20 | Treat the workspace as one project; skip the multi-project loop | Accepted |
| D-002 | 2026-04-20 | Defer hardening commits to one terminal one-liner (sandbox can't release `.git/*.lock`) | Accepted |
| D-003 | 2026-04-20 | Compress portrait to 1600 px, quality 82, progressive JPEG; keep original as dotfile | Accepted |
| D-004 | 2026-04-20 | No service worker, no WebP, no PWA shell — site is small enough | Accepted |
| D-005 | 2026-04-20 | Password gate stays as client-side obscurity; threat model documented | Accepted |
| D-006 | 2026-04-20 | Validator is stdlib-only Python, five checks, zero network, <100 ms | Accepted |
| D-007 | 2026-04-20 | Arch template uses `{{TOKEN}}` find-and-replace, no engine | Accepted |
| D-008 | 2026-04-21 | Odd-singleton project card centering scoped to `:not(.protected)` — never spotlight a locked card | Accepted |
| D-009 | 2026-04-21 | Card fade-up cascade gated to first page load via `body.first-load`; removed 1.5s after load | Accepted |
| D-010 | 2026-04-21 | Protected card unlock trigger is the semantic `<button class="lock-btn">` — no `role="button"` on the `<article>` | Accepted |
| D-011 | 2026-04-21 | "Technical Jargon" link label replaced with "Architecture" — state what's there, skip the irony | Accepted |
| D-012 | 2026-04-21 | About-tab entrance fades in each activation; prefers-reduced-motion disables it | Accepted |
| D-013 | 2026-04-21 | Em-dashes pruned from hero copy per voice rules; `.hero-byline::before` pseudo-dash removed | Accepted |
| D-014 | 2026-04-21 | `.amp` ornament span removed from hero headline; plain period instead | Accepted |
| D-015 | 2026-04-21 | Company-wall logo strip removed from About tab; experience timeline carries the same info with more context | Accepted |
| D-016 | 2026-04-21 | `.project-number` switched from serif italic to mono so all card metadata shares one voice | Accepted |
| D-017 | 2026-04-21 | Inline action-icon stroke-width normalized to 1.6 (matches project-icon baseline); primary CTA arrows stay at 2 | Accepted |
| D-018 | 2026-04-21 | `.project-status` and `.tag` font-size bumped 0.64→0.7rem for readability; mobile `.tag` 0.66→0.68rem | Accepted |
| D-019 | 2026-04-21 | Modal error color extracted to `--danger` token; single source of truth for destructive UI signals | Accepted |
| D-020 | 2026-04-21 | Modal input focus timeout bumped 30→60ms to clear iOS keyboard race | Accepted |

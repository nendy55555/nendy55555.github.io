# SESSION-STATE — thomasnendick.com

Last updated: 2026-07-08. Overwrite this file at the end of every
session — it should always describe "where we left off," not a history.

## Completed this session

- **Added World Cup Boyz card** (`https://worldcup.thomasnendick.com/`)
  at position № 03 in the Active tab, per Thomas's request. Verified
  the live site content first (FIFA World Cup 2026 snake-draft tracker,
  ESPN Soccer API, ESPN live data) so the description/tags are accurate,
  not guessed. Tags: Sports, Bracket. Status: Live. Icon: globe outline
  (international-tournament fit, distinct from the trophy icon already
  used by Dynasty Fantasy Football).
- **Renumbered all 14 cards** sequentially (№01–14) and fixed the
  `tab-count` span, which had been stale at `(12)` even before this
  session's edit (13 cards existed pre-edit; only 12 was shown).
- **No "Architecture" secondary link was added for World Cup Boyz.**
  All other Live/In-Build cards link to a `docs/architecture/<slug>.html`
  writeup; World Cup Boyz only has "Open project." Reason: writing a
  credible architecture page requires real implementation details
  (stack, data flow, hosting) that weren't available — global rule is
  "never guess env/API/data models." **Next step if Thomas wants
  parity:** copy `docs/architecture/_template.html` →
  `world-cup-boyz.html`, get real details from Thomas, wire the link
  into the card (`index.html`, World Cup Boyz `<article>`, currently
  ~line 2353).
- **Full aesthetic redesign — Ralph Lauren × Apple direction.**
  Confirmed with Thomas via two choices before touching CSS:
  cream-forward tone (kept the existing warm parchment background) +
  hunter-green/brass accent (replaced the prior terracotta-orange
  accent system). Every color in the site is a CSS custom property in
  `:root` / `[data-theme="dark"]`, so this was a token-only swap — no
  structural HTML/JS changes. New tokens, contrast-checked against WCAG
  AA with a script (all pass; see comments next to each token in
  `index.html`):
  - `--text` → deep navy ink (`#12192B` light / stays cream `#F3ECE0` dark)
  - `--accent` scale → muted brass (`#A9812E` / `#7C5D1F` / `#644B18` light,
    brighter brass `#D4A94F` / `#DEBB6C` / `#E6C883` dark)
  - `--live` (status pill color) → hunter green (`#2F5233` light,
    `#6FA876` dark)
  - `--bg` dark theme → deep navy (`#0B1220`, was warm near-black `#14110D`)
  - `--danger` (modal error) intentionally **untouched** — functional
    color, not brand-decorative, changing it risked an accessibility
    regression for no clear benefit
  - `--rule` / `--rule-soft` (hairline dividers) intentionally
    **untouched** — neutral, not accent-driven
  - JS theme-color meta swap (`colors.dark`) updated to match new dark bg
- Ran `python3 scripts/validate.py` after all edits — **PASS** (76 links,
  18 ids, 83 classes, 790 tags, 18 assets, 0 issues). The 83 informational
  notices are pre-existing unused-CSS-selector notes in the architecture
  pages, unrelated to this session.
- Could **not** get a browser screenshot of the redesign — this sandbox
  has no Chromium/deps and no sudo (`playwright install --with-deps`
  fails on the container's sudo lockdown). Verified structurally instead
  (brace balance, card count, token contrast math) but **the redesign has
  not been visually confirmed. Recommend Thomas open the site locally
  and eyeball both light and dark mode before considering this done.**
- Created this file and `QUICKSTART.md` in `docs/agent/` per Thomas's
  global workflow preference, so future sessions don't have to
  re-discover the project from scratch.

## Completed later in this session

- **Logo cropped and wired in.** Thomas resolved the upload blocker by
  dragging the file into `Website/assets/` directly (found as
  `unnamed (1).png`). Cropped via PIL/numpy flood-fill (see D-022) into
  `assets/shield-logo.png` (transparent), plus `favicon.png` and
  `apple-touch-icon.png`. Added favicon `<link>` tags (site had none
  before) and a new fixed `.brand-mark` top-left crest that mirrors the
  `.theme-toggle` button's positioning pattern. Original preserved as
  gitignored `assets/.shield-logo.original.png`. `scripts/validate.py`
  still PASSes (79 links, 22 assets, 0 issues).
- Two intermediate debug PNGs from the crop process couldn't be deleted
  (same sandbox permission issue as D-002 — bind-mount blocks unlink).
  Renamed to `._debug_transparent*.png` so the existing `._*` gitignore
  rule picks them up instead of leaving stray untracked files.

## Pushed

- **Live as of commit `7bd3721`**, pushed to `origin/main`
  (`faeb789..7bd3721`). Confirmed on GitHub's remote ref via `git
  fetch`. `thomasnendick.com` was still serving the old build a few
  seconds after push (GitHub Pages build lag, ~30-60s typical) — worth
  a re-check next session if not already confirmed live by Thomas.
- **This took four attempts from the host terminal**, not one. Every
  attempt hit a *different* stale `.git/*.lock` file left by earlier
  sandbox-side git operations this same session
  (`index.lock`, then `refs/heads/main.lock`, then `HEAD.lock`). What
  finally worked: `find .git -name "*.lock" -delete` before commit —
  sweep all lock files at once instead of removing them one at a time
  as each new one surfaces. **Add this as a documented step in
  `RUNBOOK.md`'s deploy section** if this recurs — D-002 already
  documents the root cause (sandbox bind-mount can't unlink inside
  `.git/`), but the "just run it from the host terminal" mitigation
  isn't sufficient by itself when the sandbox has already left behind
  multiple different lock files in the same session. The host terminal
  CAN delete them (regular `rm -f`, no `chflags` needed) — the earlier
  guess that this might be a permission/immutable-flag issue was wrong.

## Known inconsistency (not fixed, flagged only)

- Shared Calendar (`№ 14`, unprotected) currently sits *after* the
  three protected cards (Betting Tracker, Betting Model, Financial
  Tracker) in the Active tab. That contradicts the standing rule
  ("protected cards always hold the highest numbers, nothing
  unprotected sorts below them" — see feedback memory
  `website_project_order`). This predates this session's edits; it
  wasn't touched because Thomas's request was scoped to inserting
  World Cup Boyz at position 3, not reordering the tail. Flagging in
  case it's an oversight worth fixing separately.

## Next session should start by

1. Reading this file, then `QUICKSTART.md`.
2. Confirming the push (see Pending above) actually landed — check
   `git log` and the live GitHub Pages URL.
3. Asking whether the Shared Calendar / protected-card ordering
   inconsistency above should be corrected.

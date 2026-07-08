# QUICKSTART — thomasnendick.com

Read this before `SESSION-STATE.md`. This is the map; SESSION-STATE is
the "where we left off." Both live in `docs/agent/`.

## What this project is

A static personal site (`index.html`, single file, no build step) that
indexes Thomas's shipped side projects — each one a card with a status
(Live / In Build / Archived / Private), tags, and a link out to the
deployed app. Deployed via GitHub Pages. No backend, no package.json,
no Node, no Claude API dependency at runtime.

## File map — read only what the task needs

| File | Read when... |
|------|--------------|
| `index.html` | Almost always — this is the entire site (HTML + CSS + JS in one file) |
| `docs/agent/RUNBOOK.md` | Adding/retiring a card, changing the hero, rotating the password, deploying |
| `docs/agent/DECISIONS.md` | Before touching something that looks arbitrary — check if it was a deliberate call first |
| `docs/agent/adr-log.md` | One-line index of every decision in DECISIONS.md |
| `docs/agent/AUDIT.md` | Security/privacy posture, threat model for the password gate |
| `docs/architecture/<slug>.html` | Per-project "Architecture" pages linked from cards — voice-matched writeups, not real infra docs |
| `docs/architecture/_template.html` | Copy this to scaffold a new architecture page |
| `scripts/validate.py` | Run before considering any edit done — stdlib-only, ~30ms, checks links/ids/classes/tags/asset-size |

## Non-obvious rules (see DECISIONS.md for full reasoning)

- **Protected cards always sort last.** Betting Tracker, Betting Model,
  Financial Tracker are password-gated (`class="project-card protected"`)
  and must hold the highest `№` numbers in the Active tab. New cards
  insert above the protected block, never below. [[feedback memory:
  website_project_order]]
- **Numbering is sequential with no gaps.** Renumber every `№ XX` when
  inserting or removing a card.
- **Tab count must match card count.** `<span class="tab-count">(N)</span>`
  in the Army tab button.
- Colors are 100% CSS custom properties in `:root` and
  `[data-theme="dark"]` — never hardcode a hex value anywhere else in
  the file.
- Password gate (`PROTECTED_PASSWORD` JS constant) is documented
  obscurity, not real security — see D-005 in DECISIONS.md. Don't
  "fix" it into something stronger without discussing scope with Thomas.

## Standard workflow for this project

1. Read `SESSION-STATE.md` for in-flight work.
2. Make the edit in `index.html` directly (it's the only file that
   usually changes).
3. Run `python3 scripts/validate.py` — must PASS.
4. If a visual/CSS change: describe it can't be screenshotted from this
   sandbox (no browser deps, no sudo) — ask Thomas to eyeball it via
   `python3 -m http.server 8000` locally, or note the limitation.
5. Update `DECISIONS.md` + `adr-log.md` if the change involved a
   non-obvious tradeoff. Update `SESSION-STATE.md` at the end either way.

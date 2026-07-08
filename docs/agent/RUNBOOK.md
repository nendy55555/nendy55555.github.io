# RUNBOOK — thomasnendick.com

How to edit the site without Claude. Every common task below should take
under ten minutes once you have the repo cloned and your editor open.

**Project root:** `~/Documents/Claude/Projects/Website`

---

## Preview locally

Static HTML. No build. Two options, both run in one terminal line.

**Fastest — native macOS Python:**

```bash
cd ~/Documents/Claude/Projects/Website
python3 -m http.server 8000
```

Open http://localhost:8000. Takes under 5 seconds.

Ctrl-C to stop.

---

## Run the validator before you commit

```bash
cd ~/Documents/Claude/Projects/Website
python3 scripts/validate.py
```

Runs in ~25 ms. Checks links, duplicate IDs, CSS orphans, tag balance, and
the 1 MB asset budget. Returns exit code 0 on PASS, 1 on FAIL.

Re-run with `--verbose` to see informational notices.
Re-run with `--strict` to fail on notices too.

---

## Add a new project card

You'll edit two files: `index.html` (the card) and `docs/architecture/<slug>.html`
(the architecture page). Estimated time: 10–15 minutes.

### Step 1 — create the architecture page

```bash
cd ~/Documents/Claude/Projects/Website/docs/architecture
cp _template.html <slug>.html
```

Open `<slug>.html` and replace every `{{TOKEN}}` (instructions sit inside
the file). Use an existing live page (`housing-finder.html`,
`grocery-shopper.html`) as a voice reference.

### Step 2 — add the card to index.html

Open `index.html` and find the `#projects-active` grid (search for
`<!-- Active projects -->`). Copy an existing card and swap its fields.

Critical fields on the card:

- `data-number="NN"` — two-digit project number
- `data-status` — one of: `live`, `in-build`, `archived`, `private`
- `data-arch-url="docs/architecture/<slug>.html"` — must match the file
- `href=` on the primary link — the deployed URL, or `javascript:void(0)`
  for In Build

### Step 3 — preserve numbering rule

Protected cards (Betting Tracker, Betting Model) **always** sit at the
bottom of the Active list and hold the highest `№` values. If you add a
card, renumber the protected cards up. Do not leave gaps.

### Step 4 — verify

```bash
cd ~/Documents/Claude/Projects/Website
python3 scripts/validate.py
python3 -m http.server 8000
```

Click the new card. Click the "architecture" link. Everything should land.

---

## Retire a project card

Remove the card block from `index.html`, then delete the matching file
from `docs/architecture/`. Run the validator. A dangling arch file is
technically harmless (nothing links it) but it will rot.

```bash
cd ~/Documents/Claude/Projects/Website
git rm docs/architecture/<slug>.html
# edit index.html to remove the card
python3 scripts/validate.py
```

---

## Change the hero thesis

Search `index.html` for `<header class="hero">`. The headline sits in
`.hero-byline`, the lede in `.hero-sub`. Keep them short. The voice rules:

- Active verbs, human subject.
- No em-dashes. No adverbs.
- Vary rhythm. Short sentence next to a longer one.

Preview before you commit.

---

## Rotate the password gate

The password lives in `index.html` as a JavaScript constant. Search for
`PROTECTED_PASSWORD`.

```javascript
const PROTECTED_PASSWORD = 'nendick'; // change this
```

**This is obscurity, not security.** Anyone who opens DevTools → Sources
can read the value. See `docs/agent/AUDIT.md` for the threat model. If
you ever protect something that actually matters, move the gate to a
server with a shared-secret check.

---

## Swap the portrait image

1. Save the new file in `assets/` with a stable name (e.g. `headshot.jpg`).
2. If the new file is over 1 MB, compress it first:

   ```bash
   cd ~/Documents/Claude/Projects/Website
   python3 -c "
   from PIL import Image, ImageOps
   im = ImageOps.exif_transpose(Image.open('assets/NEW_FILE.jpg'))
   im.thumbnail((1600, 1600))
   im.save('assets/NEW_FILE.jpg', 'JPEG', quality=82, progressive=True, optimize=True)
   print('OK')
   "
   ```

   Takes ~3 seconds per image on an M-series Mac.

3. Save the pre-compression original as `assets/.NEW_FILE.original.jpg`
   (the dot prefix is gitignored).
4. Update the `<img src="...">` in `index.html`.
5. Run the validator — the asset budget check will fail the commit if the
   file is still over 1 MB.

---

## Deploy

The site currently serves from GitHub Pages. The deploy model is:

1. Commit changes to `main`.
2. Push to GitHub.
3. Pages picks it up on the next build cycle (~30–60 seconds).

```bash
cd ~/Documents/Claude/Projects/Website
python3 scripts/validate.py    # must PASS first
git add -A
git commit -m "<imperative subject line explaining why>"
git push origin main
```

Commit messages: explain **why**, not **what**. The diff is the what.

**If `git commit` or `git push` fails with `fatal: Unable to create
'.git/<something>.lock': File exists`:** a Claude session touched this
repo's `.git/` directory first. The sandbox's bind-mount can't unlink
files inside `.git/` (see D-002), so it leaves stale lock files behind
— and they show up one at a time, a different file each retry
(`index.lock`, then `refs/heads/main.lock`, then `HEAD.lock` have all
been seen in the wild). Don't remove them one by one. Run this first,
then commit/push normally — regular `rm`, no `sudo` or `chflags`
needed, this is a plain stale-file issue, not a permissions one:

```bash
find .git -name "*.lock" -delete
```

---

## When something breaks on production

1. Open the site, open DevTools → Console.
2. Hard-refresh (Shift-Reload) to bypass cache.
3. If fonts are missing, `fonts.googleapis.com` is the likely culprit.
   The CSS tokens (`--serif`, `--sans`, `--mono`) fall back to system
   fonts. Visual only. Not a site-down event.
4. If project links 404: the external host (Fly.io, GitHub Pages on
   another repo) moved. Update the `href` in the card.
5. If the password gate is stuck open or closed: the `sessionStorage`
   key `protected-unlocked` is controlling state. Clear site data.

Log the fix in `docs/agent/DECISIONS.md` if it was non-obvious.

---

## Dependency map (one glance)

| Dependency | Where it lives | Failure mode | Mitigation |
|------------|----------------|--------------|------------|
| Google Fonts | `<link>` in every HTML head | Visual degrade | System-font fallbacks pre-configured |
| Fly.io hosts (Grocery, Rideshare) | External project URLs | 404 on card click | Manually update href |
| GitHub Pages sub-repos | External project URLs | 404 on card click | Manually update href |
| Password obscurity | `PROTECTED_PASSWORD` constant | Leaks via View Source | Do not protect anything that matters |

No package.json. No Node. No Python runtime. No Claude API. The site
renders with a browser and a folder of files.

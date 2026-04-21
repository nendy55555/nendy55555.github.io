# thomasnendick.com — UI Features Review

**Prepared:** 2026-04-21
**Scope:** "Nice UI features" pass. Complement to `audit-and-ideas.md` (that doc covers positioning, copy, and structural polish; this one covers interaction patterns that would add editorial craft and make the site feel handmade).
**Source:** `index.html` @ ~2,723 lines; architecture pages unchanged.
**Status:** Ideas only. No code changes. Pick what to execute.

---

## Why these matter

The site already looks handmade. What it doesn't yet feel is **interactive in a way that rewards the reader.** Every interaction right now is obvious: hover lifts a card, click opens a page. That's fine — but a partner who spends 45 seconds on the page gets no second-layer reward for staying. The features below add texture without breaking restraint.

Rule of taste: one new interaction is signature, three is a toy store. Pick two or three. Keep the rest in reserve.

---

## ★ 1. Glossary tooltips (the anchor feature)

**One-line:** Hover (or tap) a specialized term, get a 1–2 sentence definition in a small editorial card. Dotted underline signals hoverability.

### Why it wins for this audience
- **Deloitte partners** see "FDE" and "Agentic AI" and can glance-check the definition without losing their place. Signals you write for mixed audiences.
- **Technical readers** see "Dynasty FF" or "Prompt Engineering" and get *your* framing, not Wikipedia's — a chance to show voice.
- **Craft signal:** glossaries are a publication convention (Monocle, Stripe Press, The New Yorker online). Nobody else's personal site does this.

### Candidate terms already on the page

| Term | Where it lives | Why it needs a gloss |
|---|---|---|
| **FDE / Forward Deployed Engineer** | Hero, About lede, About body | Half your readers won't know the Palantir-origin role |
| **Agentic AI** | Skills tag, About | Current buzzword — define *your* version |
| **Gen AI** | Skills tag | Often conflated with agentic; your def. clarifies |
| **Prompt Engineering** | Skills tag | Readers assume "writing prompts" — state the discipline |
| **Dynasty FF** | Project card | Jargon; one sentence and a non-fan gets it |
| **Operating Models** | Skills tag | Consulting term; partners know it, others won't |
| **M&A Integration** | Skills tag | Same — safe to gloss for non-consultants |
| **Engagement Economics** | Skills tag | Deloitte-speak; define in plain language |
| **Roadmapping** | Skills tag | Gloss separates yours from PM-roadmapping |
| **System Architecture** | Skills tag | Narrow your claim — which layer, what stack |
| **Live / In Build / Archive** | Status pills on cards | Gloss explains what each status means for upkeep |

~11 terms. Enough to be substantive, small enough to not feel like Wikipedia.

### Interaction model

- **Visual cue:** 1px dotted underline in `rgba(var(--text-rgb), 0.35)`. Cursor `help`.
- **Trigger (desktop):** `mouseenter` + `focusin`. Dismiss on `mouseleave` + `focusout` + `Escape`.
- **Trigger (touch):** Single tap opens, tap-outside or second tap closes. No sticky open on scroll.
- **Placement:** Floating card above the term when space allows, below otherwise. Arrow points at the term.
- **Delay:** 120ms open, 80ms close (prevents flicker on passing hover).
- **Stagger:** Only one tooltip visible at a time — opening a second dismisses the first.

### Visual spec

```
┌────────────────────────────────────────────┐
│  Forward Deployed Engineer                 │
│  ─────────────────────                     │   ← thin rust rule
│  Engineer who sits inside a client's       │
│  problem, builds the smallest thing that   │
│  answers it, and leaves the artifact       │
│  behind. Palantir-origin role.             │
│                                            │
│  § In your words                            │   ← mono kicker
└────────────────────────────────────────────┘
      ▲
      │  (dotted-underlined term)
```

- Card: `--bg-card` background, 1px `--rule` border, 8px radius, 16px 18px padding, 240px max-width
- Title: DM Sans 500, 0.9rem, `--text`
- Body: DM Sans 400, 0.85rem, line-height 1.5, `--text-secondary`
- "§ In your words" kicker: JetBrains Mono 0.66rem, `--text-muted`, 0.14em tracking, uppercase
- Shadow: `0 6px 24px rgba(30, 26, 22, 0.10)` — heavier than card hover, announces the overlay
- Arrow: 8px triangle same background + border as card

### Implementation sketch

```html
<span class="gloss" data-gloss="fde">FDE</span>

<template id="gloss-defs">
  <div data-term="fde">
    <h4>Forward Deployed Engineer</h4>
    <p>Engineer who sits inside a client's problem, builds the smallest thing
       that answers it, and leaves the artifact behind. Palantir-origin role.</p>
  </div>
  <!-- …more -->
</template>
```

```css
.gloss {
  border-bottom: 1px dotted rgba(var(--text-rgb, 30, 26, 22), 0.35);
  cursor: help;
}
.gloss-tooltip {
  position: absolute;
  z-index: 50;
  max-width: 240px;
  padding: 14px 16px;
  background: var(--bg-card);
  border: 1px solid var(--rule);
  border-radius: 8px;
  box-shadow: 0 6px 24px rgba(30, 26, 22, 0.10);
  opacity: 0;
  transform: translateY(4px);
  transition: opacity 160ms, transform 160ms;
  pointer-events: none;
}
.gloss-tooltip.open {
  opacity: 1;
  transform: translateY(0);
  pointer-events: auto;
}
```

~60 lines of JS to wire up positioning, delay, focus handling, `Escape` dismissal, and the template lookup. Keep definitions in one template block so copy edits stay in one place.

### Accessibility

- `role="button"` + `tabindex="0"` on `.gloss` spans so keyboard users reach them.
- `aria-describedby` points at the tooltip once rendered.
- `Escape` closes the active tooltip and returns focus to the term.
- `prefers-reduced-motion` disables the 4px slide-in.
- Screen-reader users get the definition in DOM order via `aria-describedby` — no extra live region needed.

### Effort
Small. 2–3 hours including copy.

### Risk
Low. One new interaction pattern, scoped to a known term list. Worst case: tooltip mis-positions at viewport edge — mitigation is a left/right flip when within 12px of the edge.

---

## The rest of the short list

Ranked by payoff for a Deloitte-partner / FDE-hiring audience, given the site's editorial tone.

### ★ 2. Footnote-style citations on claims

**One-line:** Numbered superscripts on specific factual claims — hover reveals the source or detail in the same tooltip pattern as the glossary.

Where it lives: "9 projects shipped" → ⁽¹⁾ expands to the list. "Technology Strategy Manager at Deloitte" → ⁽²⁾ expands to dates + practice. "Aspiring FDE" → ⁽³⁾ points at the `/how-i-work` page (once written).

**Why it wins:** Footnotes are *the* editorial craft signal. Every serious publication uses them. Shares 90% of the tooltip infrastructure from #1 — if you build the glossary, footnotes are ~1 hour of additional work.

**Effort:** XS after #1. M standalone.

---

### ★ 3. Copy-link anchors on headings

**One-line:** Hover a section heading, a subtle `§` icon appears. Click copies a URL with the anchor. 1.2s toast confirms.

Where: every `<h2>` and `<h3>` inside the page + architecture pages.

**Why it wins:** Deloitte partners forwarding a section link to a colleague is the exact share behavior you want. Signal of craft (every good docs site has this; no personal site bothers). Pattern: GitHub, MDN, Docusaurus.

**Effort:** S. ~40 lines of JS + CSS.

**Detail:** Place the `§` absolutely-positioned to the left of the heading, not inline — keeps the serif display from reflowing on hover. Fade in over 120ms. Use `navigator.clipboard.writeText()` with a toast fallback. Scroll-to on page load if URL contains a hash.

---

### ★ 4. Keyboard shortcut hint overlay (`?` to open)

**One-line:** Press `?` anywhere on the page, a small card rises from the bottom-right listing available shortcuts. `Esc` closes.

Shortcuts to wire up:
- `J` / `K` — cycle project cards (adds focus ring, scrolls into view)
- `1` / `2` — switch Active / Archive tabs
- `T` — toggle theme
- `G` then `H` — go home (smooth-scroll to hero)
- `G` then `A` — go to About
- `G` then `C` — go to Contact
- `?` — open this help
- `Esc` — close modal or help

**Why it wins:** Partners who notice keyboard-first sites recognize the craftsman signal immediately. Zero risk — invisible to anyone who doesn't press `?`. Linear, Superhuman, Arc all do this; nobody's personal site does.

**Effort:** M. 80–120 lines of JS. Real cost is deciding which shortcuts earn their keep.

**Detail:** Show the overlay only after the first `?` press per session — avoid it polluting first-paint. Suppress shortcuts when an input or modal is focused. Add a tiny mono footer nudge once: `Press ? for shortcuts` — 5s visible, dismissible, never re-shown.

---

### ★ 5. Scroll-progress rail (left edge)

**One-line:** A 2px vertical rule along the left edge of the viewport fills in rust as the reader scrolls. Ends at 100% at the footer.

**Why it wins:** Editorial publications use progress rails (The Atlantic, NYT longform). Makes the page feel like something with a *length* worth measuring. Tiny, elegant, invisible until noticed.

**Effort:** XS. 20 lines of CSS + 10 lines of JS.

**Detail:** `position: fixed; left: 0; top: 0; width: 2px; height: 100vh; background: var(--rule-soft);` with an inner `::before` that scales vertically based on `window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)`. Hide on `prefers-reduced-motion`. Hide below 900px width (too tight on mobile).

---

### 6. Project-card hover peek

**One-line:** After a card is hovered for 600ms, a small inline panel expands below the description showing: tech stack chips, last-updated date, and a one-line architecture teaser.

**Why it wins:** Turns the hover from "card lifts" into "card tells me one more thing." Pairs well with the status spine idea from `audit-and-ideas.md` High-05 — hover reveals *why* it's Live or In Build.

**Effort:** M. Needs per-card content and a collapse/expand animation that doesn't jank the grid.

**Risk:** Medium. Card grid reflow on hover is easy to do badly. Mitigation: reserve the peek space with `max-height` transitions, not `height: auto`. Or render the peek as an absolutely-positioned overlay that doesn't affect layout.

---

### 7. Cmd+K command palette

**One-line:** `⌘K` opens a Superhuman-style palette to jump to any project, toggle theme, open contact, or search (if search is ever added).

**Why it wins:** Only worth it once there are ~15+ destinations. With the current 9 cards + 3 sections, it's overkill. Revisit after Pass 2 of the other audit.

**Effort:** M-L.
**Verdict:** Defer.

---

### 8. Inline link previews for external project URLs

**One-line:** Hover a `fly.io` or `github.io` project link → a small card shows the site's og:image thumbnail, title, and last-deploy time. Like Obsidian's hover previews.

**Why it wins:** Turns an opaque URL into a visual preview without requiring the user to click. Pattern popularized by Notion, Obsidian, Are.na.

**Effort:** M. Needs either a build-time fetch of OG metadata (static JSON) or a lightweight runtime fetch (CORS issues likely).

**Risk:** Medium. Runtime fetch fights your "zero network" validator discipline. Static JSON (regenerated on deploy) is cleaner but adds a build step — currently you have none.

**Verdict:** Cool but a notable cost for a small win. Skip unless you're already adding a build step for something else.

---

### 9. Reading-time kicker on architecture pages

**One-line:** Each `docs/architecture/*.html` page shows a mono kicker in the masthead: `4 MIN READ · MMXXVI`.

**Why it wins:** Editorial convention. Five-minute payoff per page in writing credibility. Medium, The Atlantic, every serious long-form site does this.

**Effort:** XS. Word count × 0.0045 min/word at build time or compute client-side from `document.body.innerText.split(/\s+/).length`.

---

### 10. Annotated TOC rail for architecture pages

**One-line:** On wide screens, the architecture pages show a right-side floating TOC scroll-spying the current section. Each item is a thin mono label; active item gets the rust accent.

**Why it wins:** Architecture pages will grow — this scales as content does. Signals documentation-as-product. Stripe docs, Tailwind docs, Next.js docs all use this pattern.

**Effort:** S-M. ~60 lines of CSS + IntersectionObserver.

**Detail:** Hide below 1100px. Sticky positioning, `top: 120px`. Smooth-scroll when clicked. No URL hash update on scroll (too noisy) — only on click.

---

### 11. Text-selection micro-toolbar

**One-line:** Select any passage of prose → a tiny inline toolbar appears with `Copy quote`, `Tweet`, `Copy link to selection` (if supported).

**Why it wins:** Medium uses this; it's the single most editorial of the "nice touches." Invites sharing. Zero friction for anyone who doesn't use it.

**Effort:** S-M. 80 lines of JS. Text Fragments API (`#:~:text=`) is the one compelling use; the copy-as-quote flow is a nice bonus.

**Risk:** Low. Hide the toolbar when selection clears. Suppress in inputs and code blocks.

---

### 12. View Transitions between index and architecture pages

**One-line:** Click a `docs/architecture/*` link → the card title morphs into the architecture-page heading via the native View Transitions API.

**Why it wins:** If you do it right, a partner experiences the page as one connected document rather than two. Very 2026 — browser support hit baseline mid-2025.

**Effort:** M. Needs `@view-transition` opt-in in both pages + matching `view-transition-name` on the card title and the architecture H1.

**Risk:** Medium. Degrades gracefully (no-op on older browsers), but easy to get wrong — a mismatch between the two names makes the transition jarring.

**Verdict:** Save for Pass 3. Pairs best with the flagship case study.

---

### 13. Colophon "last edited" timestamp

**One-line:** Footer colophon gets one new line: `LAST SET · 2026-04-20 · MMXXVI`.

**Why it wins:** Signals the site is maintained. Partners re-visiting three months later see it's still tended. Editorial convention: every publication dates its issues.

**Effort:** XS. Can be static (update on deploy) or pull from `document.lastModified`.

**Detail:** Format as Roman numeral year to match the existing editorial flourish. Keep the mono typography already in the footer.

---

### 14. Live status indicator with deploy timestamp

**One-line:** Hover the `● Live` dot on a project card → tooltip shows `Last deployed: 2026-04-15`.

**Why it wins:** Makes the "Live" label accountable. Without a timestamp, Live is a claim; with one, it's evidence.

**Effort:** S once the glossary-tooltip pattern exists. Per-card data attribute.

**Risk:** Low. Data is easy to let go stale — either automate via GitHub API (build-time) or accept quarterly manual updates.

---

### 15. First-visit vs. returning-visitor signal

**One-line:** If `localStorage.firstVisit` is not set, show a subtle `NEW` dot on the volume kicker for 5 seconds. Returning visitors get a different micro-cue: the kicker reads `· CONTINUED` if nothing changed since last visit.

**Why it wins:** Invites the partner to notice what's changed. Only worth it once you have a `/now` page or frequent updates to drive the "continued" state toward something new.

**Effort:** S.

**Verdict:** Defer until there's a reason to come back.

---

### Intentionally skipped (and why)

- **Custom cursor.** Dated; fights editorial tone.
- **Parallax anywhere.** Anti-brief.
- **Animated page transitions via JS.** View Transitions API is the right tool — skip the JS hack.
- **Confetti on unlock.** No.
- **Magnetic buttons.** Trendy in 2022, cringe in 2026.
- **Audio on hover.** Unless the site has a soundtrack vision, skip.
- **Live "visitor count" widget.** Ad-tech smell.

---

## The three I'd ship first, in order

1. **Glossary tooltips** (★1). Flagship. 2–3 hours. Establishes the hover-card pattern that #2 and #14 reuse.
2. **Copy-link anchors on headings** (★3). 1 hour. Invisible until hovered; invaluable when shared.
3. **Scroll-progress rail** (★5). 30 minutes. Pure editorial signal; zero cost.

After these three, the page gains three discrete "oh, nice" moments without a single heavy-handed gesture. Everything else stays in reserve for Pass 2 of the broader audit.

---

## Open questions

1. **Glossary copy voice.** Should definitions sound *neutral-editorial* (third person, short) or *first-person-opinionated* ("FDE is the role I think strategy management should become")? I'd pick a middle path: neutral definition + one first-person line. Confirm.
2. **Which 8–11 terms** get glossed in V1? The list above is a first pass; you may want to prune consulting jargon and keep only technical terms, or vice versa depending on which audience you're optimizing.
3. **Copy-link anchors — style.** `§` is editorial. `#` is web-native. Pick one. My vote: `§`.
4. **Do you want keyboard shortcuts (★4) in the first ship?** It's a delightful touch but doubles the JS footprint. Not needed now if you're shipping the top three above.

---

*End of review. No code changes. Confirm the top three (or adjust) and I'll execute.*

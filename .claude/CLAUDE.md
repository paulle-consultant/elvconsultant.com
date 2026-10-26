# elvconsultant.com: design rules for Claude

Static site on GitHub Pages (`index.html`, `blog/`, `english/`). Single-file pages, no build step.

## Skills in this repo (`.claude/skills/`)
- `taste-skill` (design-taste-frontend, leonxlnx, MIT): art direction, house rules, `scripts/inspect.mjs` gate. Run `node .claude/skills/taste-skill/scripts/inspect.mjs index.html` before shipping a page change; 0 FAIL is the bar.
- `impeccable` (pbakaus, Apache-2.0): `/impeccable critique|audit|polish|animate …` for review and refinement.
- `emil-design-eng`, `animate`, `improve-animations`, `review-animations`, `animation-*`, `find-animation-opportunities` (Emil Kowalski, MIT): motion decisions and review.

## Design system (homepage, Oct 2026 redesign)
- Direction: "Type and nothing else" (taste-skill seed 261786366), brand palette kept.
- Font: Be Vietnam Pro 400/500/600, self-hosted in `assets/fonts/` (full Vietnamese diacritics). No Orbitron, no monospace.
- Tokens: `--bg #07111F`, `--surface #0D1A2C`, `--ink #EEF3F8`, `--muted #B4C2D3`, `--accent #00C8E0`, `--accent-ink #032A31`, `--paper #EDF2F7`.
- Chapters are full fields: `.field-dark`, `.field-deep`, `.field-paper`, `.field-accent`, each with `data-tone`; the fixed header takes the tone of the chapter under it.
- Type steps only: `--step-small`, `--step-body`, `--step-lead`, `--step-mid`, `--step-head`, `--step-display`.
- Motion: `--ease-out cubic-bezier(.23,1,.32,1)`; transform/opacity/clip-path only; every hidden start state lives inside `@media (prefers-reduced-motion: no-preference)`; buttons `scale(.97)` on `:active`; hover effects behind `(hover:hover) and (pointer:fine)`.
- Banned: eyebrow labels, 01/02 numbering, tiny uppercase tracked labels, gradients, glows, glass, icon-topped card grids, em dashes in new copy.

## Content
- All UI strings are bilingual in the `i18n` object (`en` / `vi`); `data-i18n` sets text, `data-i18n-html` sets markup.
- The interface matrix (`MATRIX` in the script) is the page's live element; keep its entries technically correct.

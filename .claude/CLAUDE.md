# elvconsultant.com: design rules for Claude

Static site on GitHub Pages (`index.html`, `blog/`, `english/`). Single-file pages, no build step.

## Skills in this repo (`.claude/skills/`)
- `taste-skill` (design-taste-frontend, leonxlnx, MIT): art direction, house rules, `scripts/inspect.mjs` gate. Run `node .claude/skills/taste-skill/scripts/inspect.mjs index.html` before shipping a page change; 0 FAIL is the bar, except the accepted luxury FAILs listed under Design system.
- `impeccable` (pbakaus, Apache-2.0): `/impeccable critique|audit|polish|animate …` for review and refinement.
- `emil-design-eng`, `animate`, `improve-animations`, `review-animations`, `animation-*`, `find-animation-opportunities` (Emil Kowalski, MIT): motion decisions and review.

## Design system (homepage, "Maison" luxury restyle, 2026-10-31)
- Direction: luxury-house look requested by Paul ("phong cách website hàng hiệu cao cấp"). Supersedes the Oct 2026 "Type and nothing else" palette.
- Fonts, self-hosted in `assets/fonts/` (full Vietnamese): display `--serif` Cormorant Garamond 400/500 + 400 italic; body Be Vietnam Pro 300 (400/500/600 kept for emphasis).
- Tokens: `--bg #0C0B09` noir, `--surface #15130F`, `--ink #F3EDE2` ivory, `--muted #B5AC9C`, `--accent #C9A96A` champagne gold, `--accent-ink #16120B`, `--sand #E6D9BF`, `--paper #F7F3EC`, `--bronze #7A5A26`.
- Fields: `.field-dark` noir, `.field-deep` deep noir, `.field-paper` ivory, `.field-accent` champagne sand. Per-field `--ac` = accent text colour that passes contrast on that field (gold on noir, bronze on ivory/sand); use `--ac`, never raw `--accent`, for text. `--line` = hairline colour.
- Signature details (deliberate, accepted inspector FAILs `micro-label`, `hairline`, `eyebrow`): uppercase tracked 13px labels/nav/buttons (`--track .16em`), 1px hairline rules instead of zebra fills, square corners (no pills), gold underline highlights.
- Type steps only: `--step-small`, `--step-body`, `--step-lead`, `--step-mid`, `--step-head`, `--step-display`; nothing under 13px.
- Motion: `--ease-out cubic-bezier(.23,1,.32,1)`; transform/opacity/clip-path only; hidden start states inside `@media (prefers-reduced-motion: no-preference)`; buttons `scale(.97)` on `:active`; hover behind `(hover:hover) and (pointer:fine)`.
- Banned: gradients, glows, glass, icon-topped card grids, 01/02 numbering, em dashes in new copy.

## Content
- All UI strings are bilingual in the `i18n` object (`en` / `vi`); `data-i18n` sets text, `data-i18n-html` sets markup.
- The interface matrix (`MATRIX` in the script) is the page's live element; keep its entries technically correct.

## Publishing (standing instruction from Paul)
- Every change to this site is committed and pushed to `origin main` right away, without asking for confirmation. GitHub Pages deploys from `main`.
- Before pushing a page change, run the taste-skill inspector; fix FAILs first.
- Never force-push and never rewrite history on `main`.
- Commit only the files you changed; leave unrelated working-tree changes (e.g. CRLF-only diffs in `english/`) alone.

## Blog theme guard
- Blog pages share `assets/maison.css`. `.github/workflows/maison-blog.yml` runs `scripts/maison_blog.py` on every push to `blog/` and auto-commits: it recolours old navy/cyan literals, removes Google Fonts and links `../assets/maison.css`. New newsletter posts end up in the luxury theme even if generated from the old template.

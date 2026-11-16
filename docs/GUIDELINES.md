# Site guidelines

Rules for the concept visuals and pages on this site. Keep new pages consistent with them.

## Proportions of screens

| Mock | Proportion | Design size | Where it lives |
| --- | --- | --- | --- |
| Phone screen (app), the display itself | **9 : 19.5** (like a modern iPhone) | 322 × 698 px (the frame adds a 9 px bezel: 340 × 716) | `.pa-screen` inside `.pa-phone` in `assets/posta-app.css` |
| Web / browser window | **16 : 9** | 840 × 473 px | `.pa-browser` in `assets/posta-app.css` |

- Both are drawn at their design size and **never stretched or squeezed**. On narrower screens `assets/app.js` (`fitMocks`) shrinks them with `zoom`, so the proportion stays exact on phones too.
- Do **not** use viewport media queries (`@media (max-width…)`) to rearrange the inside of a mock. The mock is a fixed picture, not a responsive page.
- The content of a mock must fit its frame (no scrolling inside). If a screen is too tall, remove content or tighten spacing instead of letting the frame grow.
- A phone gallery (`.pa-row`) scrolls sideways and can be dragged with the mouse; a phone next to a web window uses `.pa-pair`.

## Concept visuals

- Everything drawn by us is labelled as made with AI: the full note above the first gallery on a page, and a small **AI** tag in every caption.
- All names, numbers, amounts, branches and dates in a mock are **examples**; mark them `example` / `primer` where figures appear.
- Figures that come from a source stay in the text with the source linked; screens must not invent official fees or deadlines.

## Pages

- Every page is bilingual: Serbian (Latin) and English, both in the markup, one hidden by the language switch. Every string is a `(sr, en)` pair.
- The home page groups ideas by topic (`tools/categories.py`); the idea number is only a label, not a ranking.
- Detail pages for the main ideas use a colour of their own (`THEMES` in `tools/pages_data.py`); the screens on a page follow that colour (`pa-*` variants in `assets/posta-app.css`).
- Page order: overview cards, a big comparison, before/after, app + web screens, supporting blocks, Q&A. Prefer pictures and short lines over paragraphs.

## Build

`python3 tools/build.py` regenerates `index.html` and `idea/*/index.html` from `source/print.html`, `tools/pages_data.py` and the templates. Commit the generated files: GitHub Pages serves them as they are.

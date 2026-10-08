# Design system

The brand handbook is the Figma file [DandyLions](https://www.figma.com/design/ADAT7igJnBG5nvij5shy9V), page **01 — Brand & system**.

Pull requests [#4](https://github.com/rbijkercom/dandy-lions/pull/4)–[#7](https://github.com/rbijkercom/dandy-lions/pull/7) restyle the existing public routes. They do not add pages, CMS fields, or seed copy. Production on Vercel is that tree (`155bb0c`). Storybook is not deployed.

## What the site implements

Two themes, set with `data-theme` (aliases `.tone-light` and `.tone-sage`):

- **Light** — Insights, About, and the ivory content band on Consulting.
- **Inverted** — sage `#748262`. Consulting header, hero, and footer. There is no charcoal `tone-dark`.

Tokens live in `src/app/(frontend)/styles.css`. Primitives include ivory `#F5F2EC`, sage `#748262`, charcoal `#2D2D2D`, gold `#907948`, gold-deep `#7A663C`, pale sage `#C6CAB9`, body ink `#454340`, card surface `#FBF9F4`, and error-deep `#FF9F9F`. Semantic roles (`surface`, `text`, `button`, `field`, `focus`) inherit from the theme. Inverted errors use error-deep. The error-deep swatch label on the Figma canvas still prints `#C13535`; the variable `palette/error-deep` is `#FF9F9F`, and the app follows the variable. Do not add one-off colors or type sizes in route files.

Type is Cormorant Garamond (300, 400, 400 italic, 600) and Hanken Grotesk (400), loaded with `next/font`. Do not set `--font-serif` or `--font-sans` in CSS. Display is Cormorant Light: 44px / line-height 1.04 / letter-spacing −3% below 768px, and 60px with the same ratios from 768px up. Supporting italic is Cormorant Italic 22/30. Page ledes are Cormorant Light too (`type-lead`: 20px below 768px, 28px from 768px up, line-height 1.44). Editorial paragraphs are Cormorant Light (`type-reading`: 18–24px, line-height 1.42). Lists, card copy, labels, and controls stay Hanken Regular 400. Control labels use `type-ui-control` (12/20, 1.2px tracking); do not add a separate `type-ui-sm`. `type-lead`, `type-wordmark`, and `type-route` stay as page-specific styles. `html` uses antialiased font smoothing, matching the original site. A fixed paper-grain overlay (`body::after`, `public/brand/grain.png`, opacity 0.035) covers ivory and sage, including the split home. The mobile menu paints above it. Layout: content max 1312, reading measure 720, control height at least 44px (`--control-min`), section gap 96px, breakpoints 768 and 1200. Default buttons are 40px at 12px. Small buttons and chips are 39px at 11px. Under `@media (pointer: coarse)`, buttons use a 44px min-height tap target. Nav links and the services trigger are 34px at 12px. Menu items are 40px at 13px. A segmented tab group is 36px, with 28px segments at 11px. Section tabs stay 44px at 14px. Inverted pressed buttons use sand `#C3C0A6`. Hover lift is gold at 20% (`shadow/hover`) on Light and Inverted. There is no `sage-deep` `#646F55`; inverted surfaces are sage `#748262`. Below 768px, `--page-intro-top` is 30px and `--hero-intro-top` is 16px. The page hero is title, optional lede, and a 533×544 photo, with 64px above and 96px below.

The UI library is `src/components/ui/` (buttons, tabs, chips, fields, cards, accordion, steps, logo, icons). Pages compose those components. Icons are the custom Figma set, painted with `currentColor`. The default mark is `public/brand/logo-symbol.svg`; a Payload `logo` upload can override it. The split home still uses the charcoal and ivory lion artwork.

Chrome:

- Header is `SiteChrome`. Desktop is the pill row. At 768px and below, inner pages use the menu sheet (Radix dialog: focus trap, Escape, scroll lock).
- The split home desktop chrome follows the Mode split mockup: About pill on the ivory half, language switch and Begin the conversation on the sage half, Open ↗ on each route. Below 768px the homepage is Figma version G (side-by-side Insights/Consulting halves, lion clipped on the seam) with only a 44px burger on a transparent bar. The sheet stays portaled.
- Live pages render one legal line (`showFullFooter` is `false` in `src/lib/chrome.ts`), plus a privacy link. The full footer component remains for Storybook and includes Contact (`/contact`) and Privacy (`/privacy`). Begin opens `/contact`. Insights includes the newsletter form.
- Footer and menu strings that are not in Payload live in `chromeCopy` (EN/IT/NL) in that same file.
- Below 768px, learning topics and method loyalties are a single-open accordion. Wider viewports keep the list and panel.

`pnpm storybook` serves the library at http://localhost:6006 with Light/Inverted and EN/IT/NL toolbars. It does not open Postgres. Stories use `src/storybook/fixtures.ts`, not `src/lib/content.ts`. `storybook-static/` is gitignored. `tsconfig.build.json` excludes stories so `pnpm build` does not type-check them.

Interactive behaviour uses headless Radix for the menu sheet, tabs, accordion, and select. Visuals stay on these tokens. Do not add shadcn/ui or its theme. See [shadcn-evaluation.md](shadcn-evaluation.md).

## On the canvas, not in the app

These frames are explorations or brand material. Do not build them unless asked.

| Frame | What it is |
| --- | --- |
| Homepage — mobile concepts | Concepts A–J for a small-screen home. G (side by side) is the live mobile home. Frames F, H–J and round-1 A–E stay on the canvas. |
| Email gate, Speaker kit, Presentation kit, Stationery, Newsletter | Campaign and print layouts, plus an essay signup. Not routes. |
| Brand identity style guide | A 13-spread brand book, not site pages. |
| Icons — reference pack comparison | Phosphor, Tabler, Lucide, and others, kept for later. The app uses the custom icons. |
| 10 — Test page: Team Facilitation | A component exercise, not a service. |
| Test — Paper grain effect | An isolated Figma noise test. The site paints its own fixed grain overlay, not this frame. |
| Sitemap | The current tree (split home, About panels, Insights learning/articles/method, four services). Not a list of new URLs. |

Newsletter signup (double opt-in via Brevo), the contact form, and the privacy notice are live routes. Missing Brevo env vars pause the forms; they do not break the page.

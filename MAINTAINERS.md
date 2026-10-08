# Maintainers

**Only Ruben Bijker changes this hub.** Fabio and his Claude use it as read-only visual reference.

## What is in the hub

| Path | What | Comes from |
| --- | --- | --- |
| `design-system/tokens.json` | Curated design tokens | Site repo `rbijkercom/dandy-lions` (`src/app/(frontend)/styles.css`) and Figma file `ADAT7igJnBG5nvij5shy9V`. Edited by hand. |
| `design-system/css-tokens.json` | Raw CSS custom properties | Extracted from the site stylesheet by the daily sync. Don't edit by hand. |
| `templates/` | PNG template images: social, slides, email, brand guide | Figma file `ADAT7igJnBG5nvij5shy9V`, page "01 — Brand & system", sections "Brand identity in use" and "Brand identity style guide" (node ids in `manifest.json`) |
| `assets/logos/`, `assets/svg/` | Logo SVG/PNG files, seed graphics | Figma exports (logo formats, social pack) and the site repo (`public/`, `reference/`) |
| `assets/icons/` | Icon SVGs | Site repo `src/components/ui/Icon.tsx`, converted to standalone SVG |
| `assets/graphics/` | Paper grain texture | Site repo `public/brand/grain.png` |
| `archive/` | Historical files, not part of the active design system; not linked from the active pages | Moved out of the active hub (see `archive/README.md`) |
| `manifest.json` | List of every file with title, description, source | Edited by hand |
| `index.html`, `*/index.html`, `project-instructions.html`, `llms.txt`, `llms-full.txt` | Generated pages | `python3 scripts/build.py` |

## Rules for edits

- Public repository and public website. Add only material that is already published or cleared. No secrets, addresses, phone numbers, personal emails, company registration or VAT numbers, client names or unpublished material. (This is why the stationery kit, speaker kit, closing slide and newsletter footer are left out.)
- Real files only. Never add generated or mock-up templates. Mark gaps in `manifest.json` → `placeholders` as `[TO BE SUPPLIED BY RUBEN: ...]`.
- No copywriting or content guidance. Descriptions in `manifest.json` describe how a file looks, nothing else.
- To add an image: put the file in the right folder, add an entry to `manifest.json`, run `python3 scripts/build.py`, commit. The build reads sizes and viewBoxes from the files and fails if a listed file is missing.

## Publishing

`.github/workflows/pages.yml` runs `scripts/build.py` and deploys to GitHub Pages on every push to `main`: https://rbijkercom.github.io/dandylions-hub/

## Daily token sync

`.github/workflows/sync-from-site.yml` runs every day at 05:00 UTC (07:00 Amsterdam in summer time, 06:00 in winter) and on demand (Actions → "Sync design tokens from site" → Run workflow). Tokens only:

1. Sparse-checks out only `src/app/(frontend)/styles.css` from `rbijkercom/dandy-lions` (private), read-only.
2. Extracts the CSS custom properties into `design-system/css-tokens.json` with `scripts/extract_css_tokens.py`. The stylesheet itself is not stored.
3. If the tokens changed, opens or updates a pull request on branch `sync/site-tokens`. Ruben reviews it, updates `tokens.json` by hand where needed, and merges (merging publishes the site).

Template images and assets are not synced automatically.

### Secret you must add

- **Name:** `DANDY_LIONS_READ_TOKEN`
- **Type:** fine-grained personal access token
- **Resource owner:** rbijkercom. **Repository access:** only `rbijkercom/dandy-lions`
- **Permissions:** Repository → Contents: **Read-only** (Metadata: Read-only is added automatically). Nothing else.
- **Where:** this repo → Settings → Secrets and variables → Actions → New repository secret.
- Set an expiry and renew it before it lapses.

Without the secret the sync job stops with a clear error and changes nothing.

The workflow opens pull requests with the built-in `GITHUB_TOKEN`; Settings → Actions → General → Workflow permissions has "Allow GitHub Actions to create and approve pull requests" switched on.

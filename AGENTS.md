# AGENTS.md

GitHub **profile README** for Shrey Singh (`MrPanda009`). It is published by pushing this folder to the public repo `MrPanda009/MrPanda009`; GitHub shows its root `README.md` on the profile page.

The whole page is a stack of hand-written, animated SVGs in a 1-bit, 90s pixel-art style, in a light and a dark theme. `Refernce.png` (light) and `Reference-dark.png` (dark) are the full-page design mockups — treat them as the source of truth for look and content. (The light filename's typo is intentional; don't rename it.)

**Section order deliberately differs from the mockups:** the owner moved FEATURED_PROJECTS to the end. README order is hero → ABOUT_ME/CURRENTLY → TECH_STACK/GITHUB_STATS/LET'S_CONNECT → link row → FEATURED_PROJECTS. The mockups' footer strip ("EXPLORING IDEAS…") isn't built.

## Layout

```
README.md                         stacks the SVGs as <picture> blocks + one HTML link row
Refernce.png / Reference-dark.png design mockups (look and content; order differs, see above)
assets/Hero-Banner.svg            name, badge, tagline, clouds + panda landscape
assets/bento-about-currently.svg  ABOUT_ME + CURRENTLY_ windows
assets/bento-bottom.svg           TECH_STACK + GITHUB_STATS + LET'S_CONNECT windows
assets/dark/*.svg                 GENERATED dark variants — never edit by hand
scripts/build-themes.py           builds assets/dark/ and lints colour usage
scripts/build-stats.py            fills GITHUB_STATS from the GitHub API, then runs build-themes
.github/workflows/update-stats.yml runs build-stats daily and commits any change
```

Still to build, stubbed as HTML comments at the end of `README.md` in `<picture>` form: `header-projects.svg` and three `card-*.svg` project cards at `width="32%"`, each wrapped in a link. Build them, run the theme build, then uncomment their blocks.

## Live GitHub stats

The GITHUB_STATS window in `bento-bottom.svg` is part hand-written, part generated:

- `scripts/build-stats.py` rewrites **only** the content between `<!-- stats:start -->`/`<!-- stats:end -->` (repos, all-time commits, followers, following) and `<!-- grid:start -->`/`<!-- grid:end -->` (last 30 weeks of the contribution calendar, plus a blinking frame on today's cell). Never hand-edit inside those markers; everything around them is normal hand-written SVG.
- Numbers come from the real API — never type stats in by hand. Values ≥ 1000 render as `1k+`, `2.3k+` etc.
- Grid levels use `#cell-0`…`#cell-4` (`faint` empty cell → 25/50/75 % coral dithers → solid coral), placed with `<use x y>` so each cell's dither starts at its own corner.
- The workflow runs daily (03:17 UTC) and on demand from the Actions tab. It uses the built-in token, which only sees public contributions; the owner can add a `STATS_TOKEN` repo secret (a PAT) to count private commits.
- Run locally with `python3 scripts/build-stats.py` (uses `$GITHUB_TOKEN`, `$GH_TOKEN` or `gh auth token`).

## Links

Links inside README images can't be clicked, so the LET'S_CONNECT window is visual only and a centered HTML link row sits right under the bento in `README.md`. Owner's links: GitHub `github.com/MrPanda009`, LinkedIn `linkedin.com/in/shrey-singh-70898237b/`, X `x.com/MrPanda009w`, email `shrey33005@gmail.com`. Portfolio is "(soon)" — no link yet.

## Light and dark themes

GitHub picks the image per visitor theme via `<picture>`: the `<source media="(prefers-color-scheme: dark)">` points at `assets/dark/<name>.svg`, the `<img>` at the light `assets/<name>.svg` (also the fallback). Every image in `README.md` must use this form.

**The light SVG is the only source.** Each one holds all of its colours in a single palette block inside `<style>`:

```css
/* palette:start */
:root { --bg: #F4EFE6; --ink: #181818; ... }
/* palette:end */
```

and everything else uses role classes (`.bg`, `.ink`, `.coral`, `.st-ink`, …) or `url(#pattern)` fills — **never a hex, `rgb()` or named colour in a `fill`/`stroke` attribute or CSS rule.** The one exception is `fill="white"` inside a `<mask>`, which is luminance, not a colour.

After any SVG change:

```sh
python3 scripts/build-themes.py          # writes assets/dark/, fails on hardcoded colours or bad XML
python3 scripts/build-themes.py --check  # exit 1 if assets/dark/ is stale (use before committing / in CI)
```

A new colour role needs a value in the file's palette block **and** in `DARK` in `scripts/build-themes.py`; the build fails otherwise.

## How GitHub renders these SVGs (hard constraints)

README SVGs are displayed through `<img>`, which means:

- **No JavaScript, no external resources.** External fonts, images, `@import` and `<foreignObject>` HTML are blocked or stripped. Everything must be inline in the file.
- **CSS animations and `<use href="#id">` work.** SMIL is avoided; use CSS `@keyframes` in a `<style>` block inside `<defs>`.
- **No interactivity.** Hover states and links inside an SVG do nothing; make a section clickable by wrapping the `<img>` in an `<a>` in `README.md`.
- **Fonts come from the viewer's OS.** Text uses the monospace stack below and renders slightly wider or narrower per platform — leave ~10% horizontal slack after any text that sits near a border.
- **Each SVG paints its own background** (`<rect class="bg">`) so it never shows GitHub's page colour through.
- **A `<clipPath>` may only `<use>` a single shape, never a `<g>`** — Chrome silently clips everything away. To clip to a group, use a `<mask>` with the `<use>` filled `white` (see the hero's cloud banks).

## SVG must be valid XML

A single parse error makes the image silently disappear on GitHub. This has already happened once (a bare `&` inside a CSS comment).

- Escape `&` as `&amp;` and `<` as `&lt;` everywhere — text, attributes **and** `<style>` content, comments included.
- Never put `--` inside an XML comment (`<!-- ... -->`), e.g. CSS custom-property names like `--d`.
- Check every file before finishing:

  ```sh
  xmllint --noout assets/*.svg
  ```

## Design system

Reuse these roles; copy shared `<defs>` (patterns, sprites) and the role classes from `Hero-Banner.svg` rather than inventing new ones. Pick the role by what a thing *is*, not by its light-mode colour — two things that are both `#181818` in light mode can need different roles in dark mode.

| Role (`--var`) | Light | Dark | Use |
|---|---|---|---|
| `bg` | `#F4EFE6` | `#12110F` | canvas, window fills, cut-outs and gaps |
| `ink` | `#181818` | `#F4EFE6` | line art, text, icons, dither dots — inverts |
| `accent` | `#FF4E42` | `#FF4E42` | the single coral accent (sun, cursor, active state) |
| `accent-hi` | `#FF766B` | `#FF766B` | top bevel on coral blocks only |
| `muted` | `#7A756C` | `#6B665E` | inactive tracks/outlines only |
| `faint` | `#DDD7CC` | `#2A2824` | empty contribution cells (just off the canvas colour) |
| `shade` | `#181818` | `#12110F` | mountain shadow faces — stay dark in both themes |
| `snow` | `#F4EFE6` | `#F4EFE6` | ridge highlights, planet specular — always cream |
| `fur` / `fur-ink` | `#F4EFE6` / `#181818` | same | the panda's face and patches — never invert (a plain swap makes it a photo negative) |

- Fill classes: `.bg`, `.ink`, `.coral`, `.coral-hi`, `.shade`, `.snow`, `.fur`, `.fur-ink`, `.faint`. Stroke classes: `.st-bg`, `.st-ink`, `.st-muted`, `.st-snow`, `.st-fur-ink`, `.st-coral`. Only define the ones a file uses.
- Tech logos are drawn as single-colour ink icons in both themes (the dark mockup's cyan React is intentionally not copied: coral is the only accent).
- Dark mode follows `Reference-dark.png`: cream line art on warm black, coral unchanged, mountains as dark shapes with cream ridge lines, panda still white-faced.
- Font stack (all text): `ui-monospace, 'Cascadia Code', 'Source Code Pro', Menlo, Consolas, 'Courier New', monospace`. Headings/labels are UPPERCASE with `_` separators (`ABOUT_ME`, `CURRENTLY_`).
- Shading is **dither patterns, never gradients or transparency**: `dither-12`, `dither-25`, `dither-50`, `dither-75`, `dither-red`, `water-lines`. Patterns use `patternUnits="userSpaceOnUse"`; when shifting a group that uses them, translate by a multiple of 24 px (LCM of the 4/6/8 px tiles) so the dither grid stays aligned.
- Reusable sprites: `#star-sparkle` (2-frame 4-point star), `#star-plus`, `#pixel-title-glyphs` (6 px grid), `#icon-folder`, `#icon-bars`, `#icon-link`, `#window-dots`, `#tile`.
- Windows/cards: 2.5 px ink stroke, `rx="8"`, header icon + title + `o o o` dots (dots at `x = width − 50`, or −44 when tight), 2 px divider at y 36. A title that nearly fills its header gets `textLength` + `lengthAdjust="spacingAndGlyphs"` so wider OS fonts can't push it into the dots (see LET'S_CONNECT).
- Set `shape-rendering="crispEdges"` (root or per group) so edges stay pixel-sharp.

## Canvas sizes

All sections are full-width strips stacked with `width="100%"` and `align="top"`, so every full-width SVG uses a **viewBox width of 1000** with a 50-ish px side margin to line up with its neighbours. Current heights: hero `1000×430`, about/currently bento `1000×354`, bottom bento `1000×210` (windows at x 50 / 362 / 704, widths 300 / 330 / 246, 12 px gaps). Keep the cream colour running edge-to-edge so stacked images read as one page.

## Animation rules (90s pixel-art motion)

The owner explicitly wants every animation to feel like an old sprite game:

- **Hard frame cuts only:** `animation-timing-function: steps(1, end)` with explicit keyframes. No easing, no `linear` tweens.
- **1-bit visibility:** `opacity` is only `0` or `1`. No fades.
- **Whole-pixel motion only:** integer `translate` offsets (2 px, 4 px). No `scale`, no animated `rotate`.
- **Frame swaps over tweens:** draw each frame and toggle visibility (see `.f1`/`.f2` sparkle, `.flare-long`/`.flare-short`).
- Low frame rates (~0.15–0.6 s per frame) and staggered delays so things don't blink in sync.
- **Never animate `transform` on an element that also has a `transform` attribute** — the CSS overrides the attribute and the element jumps to (0,0). Put the animation class on an inner `<g>` instead.
- Keep `@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }` in every file.

## Verifying a change

1. `python3 scripts/build-themes.py` then `xmllint --noout assets/*.svg assets/dark/*.svg` — both must succeed silently (apart from the build's `wrote …` lines).
2. Render a still: `qlmanage -t -s 2000 -o <tmp-dir> assets/<file>.svg` and compare against the matching part of `Refernce.png`; do the same for `assets/dark/<file>.svg` against `Reference-dark.png`.
3. Check both themes the way GitHub shows them: serve the repo (`python3 -m http.server`), open a page with the same `<picture>` markup as `README.md`, and toggle the browser/OS colour scheme (Playwright: `page.emulateMedia({ colorScheme: 'dark' })`). Confirm the right file loads, nothing overlaps, text isn't clipped and frames switch cleanly.

## Content facts

Keep copy consistent with the mockup: name **SHREY SINGH**, handle **MrPanda009**, B.Tech CSE @ MUJ, project repos under `github.com/MrPanda009/` (`SETU-DRR`, `Nyay-AI-Liard`, `AWS-Auditor`). The mockups' stat numbers are placeholders — real ones come from `build-stats.py`. Don't invent stats or links — ask the owner.

# AGENTS.md

GitHub **profile README** for Shrey Singh (`MrPanda009`). It is published by pushing this folder to the public repo `MrPanda009/MrPanda009`; GitHub shows its root `README.md` on the profile page.

The whole page is a stack of hand-written, animated SVGs in a 1-bit, 90s pixel-art style. `Refernce.png` (filename typo is intentional, don't rename) is the full-page design mockup — treat it as the source of truth for layout, content and look.

## Layout

```
README.md                         stacks the SVGs, nothing else
Refernce.png                      design mockup (top → bottom = README order)
assets/Hero-Banner.svg            name, badge, tagline, panda landscape
assets/bento-about-currently.svg  ABOUT_ME + CURRENTLY_ windows
```

Planned sections are stubbed as HTML comments in `README.md` (`header-projects.svg`, three `card-*.svg` project cards at `width="32%"` wrapped in links, `bento-bottom.svg`). Build them in that order, then uncomment their block.

## How GitHub renders these SVGs (hard constraints)

README SVGs are displayed through `<img>`, which means:

- **No JavaScript, no external resources.** External fonts, images, `@import` and `<foreignObject>` HTML are blocked or stripped. Everything must be inline in the file.
- **CSS animations and `<use href="#id">` work.** SMIL is avoided; use CSS `@keyframes` in a `<style>` block inside `<defs>`.
- **No interactivity.** Hover states and links inside an SVG do nothing; make a section clickable by wrapping the `<img>` in an `<a>` in `README.md`.
- **Fonts come from the viewer's OS.** Text uses the monospace stack below and renders slightly wider or narrower per platform — leave ~10% horizontal slack after any text that sits near a border.
- **Each SVG paints its own cream background** (`<rect class="bg">`) so it looks identical on GitHub's light and dark themes.

## SVG must be valid XML

A single parse error makes the image silently disappear on GitHub. This has already happened once (a bare `&` inside a CSS comment).

- Escape `&` as `&amp;` and `<` as `&lt;` everywhere — text, attributes **and** `<style>` content, comments included.
- Never put `--` inside an XML comment (`<!-- ... -->`), e.g. CSS custom-property names like `--d`.
- Check every file before finishing:

  ```sh
  xmllint --noout assets/*.svg
  ```

## Design system

Reuse these exact values; copy shared `<defs>` (patterns, sprites) from `Hero-Banner.svg` rather than inventing new ones.

| Token | Value | Use |
|---|---|---|
| cream | `#F4EFE6` | background, cut-outs |
| ink | `#181818` | all line art and text |
| coral | `#FF4E42` | single accent (sun, cursor, active state, highlights) |
| coral light | `#FF766B` | top bevel on coral blocks only |
| muted | `#7A756C` | inactive tracks/outlines only |

- Shared CSS classes: `.bg`, `.ink`, `.coral`, `.cream`.
- Font stack (all text): `ui-monospace, 'Cascadia Code', 'Source Code Pro', Menlo, Consolas, 'Courier New', monospace`. Headings/labels are UPPERCASE with `_` separators (`ABOUT_ME`, `CURRENTLY_`).
- Shading is **dither patterns, never gradients or transparency**: `dither-12`, `dither-25`, `dither-50`, `dither-75`, `dither-red`, `water-lines`. Patterns use `patternUnits="userSpaceOnUse"`; when shifting a group that uses them, translate by a multiple of 24 px (LCM of the 4/6/8 px tiles) so the dither grid stays aligned.
- Reusable sprites: `#star-sparkle` (2-frame 4-point star), `#star-plus`, `#pixel-title-glyphs` (6 px grid), `#icon-folder`, `#window-dots`.
- Windows/cards: 2.5 px ink stroke, `rx="8"`, folder icon + title + `o o o` dots in the header, 2 px divider under it.
- Set `shape-rendering="crispEdges"` (root or per group) so edges stay pixel-sharp.

## Canvas sizes

All sections are full-width strips stacked with `width="100%"` and `align="top"`, so every full-width SVG uses a **viewBox width of 1000** with a 50-ish px side margin to line up with its neighbours. Current heights: hero `1000×430`, about/currently bento `1000×354`. Keep the cream colour running edge-to-edge so stacked images read as one page.

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

1. `xmllint --noout assets/*.svg` — must print nothing.
2. Render a still: `qlmanage -t -s 2000 -o <tmp-dir> assets/<file>.svg` and compare against the matching part of `Refernce.png`.
3. Check animation the way GitHub shows it: serve the repo (`python3 -m http.server`) and open a page that embeds the SVGs as `<img width="100%">`, mirroring `README.md`. Confirm nothing overlaps, text isn't clipped and frames switch cleanly.

## Content facts

Keep copy consistent with the mockup: name **SHREY SINGH**, handle **MrPanda009**, B.Tech CSE @ MUJ, project repos under `github.com/MrPanda009/` (`SETU-DRR`, `Nyay-AI-Liard`, `AWS-Auditor`). Don't invent stats or links — ask the owner.

"""Seeded, opaque SVG print texture for the whole README sheet.

Applied only to final composites/slices; hand-written sources and their dark twins
remain clean. Marks use page coordinates so every linked slice shares one sheet.
Only existing theme roles are used; no filters, bitmaps, fades or external assets.
"""

import random
import re
import xml.etree.ElementTree as ET

import sheet


def rect(x, y, w, h):
    return (x, y, w, h)


def texture(height):
    """Opaque, seeded print marks in page coordinates: no bitmap, filter or fade."""
    rng = random.Random(92026)
    marks = {key: [] for key in ("fiber", "dust", "ink", "chip", "edge")}
    # Broken horizontal paper fibers; many tiny marks instead of a repeating tile.
    for y in range(2, int(height), 3):
        for _ in range(rng.randint(8, 16)):
            marks["fiber"].append(rect(rng.randrange(1000), y, rng.randint(2, 9), 1))
    for _ in range(int(height * 12)):
        marks["fiber"].append(rect(rng.randrange(1000), rng.randrange(int(height)), 1, 1))
    for _ in range(int(height * 2.4)):
        marks["dust"].append(rect(rng.randrange(1000), rng.randrange(int(height)), rng.choice([1, 1, 2]), 1))
    for _ in range(int(height * 0.9)):
        marks["ink"].append(rect(rng.randrange(1000), rng.randrange(int(height)), 1, 1))
    # Missing ink in text, window rules, sprites, and the coral sun.
    for _ in range(int(height * 5)):
        marks["chip"].append(rect(rng.randrange(1000), rng.randrange(int(height)), rng.choice([1, 1, 2, 3]), 1))
    for _ in range(1500):
        marks["chip"].append(rect(rng.randrange(50, 285), rng.randrange(62, 170), rng.randint(1, 3), 1))
    for _ in range(1400):
        marks["chip"].append(rect(rng.randrange(885, 1000), rng.randrange(45, 215), rng.randint(1, 3), 1))
    # Ragged, incomplete border and concentrated abrasion at the paper edges.
    for x in range(14, 986):
        if rng.random() < 0.72:
            for y in (9, int(height) - 10):
                marks["edge"].append(rect(x, y + rng.choice([-1, 0, 0, 1]), 1, 1))
    for y in range(14, int(height) - 14):
        if rng.random() < 0.72:
            for x in (9, 990):
                marks["edge"].append(rect(x + rng.choice([-1, 0, 0, 1]), y, 1, 1))
    for _ in range(int(height * 5)):
        x, y = rng.randrange(1000), rng.randrange(int(height))
        edge_distance = min(x, 999 - x, y, height - 1 - y)
        if edge_distance < 5 + rng.random() ** 3 * 27:
            marks["edge"].append(rect(x, y, rng.choice([1, 1, 2, 3]), 1))
    return marks


def path_for(marks, x, y, w, h):
    return "".join(
        f"M{px-x:g},{py-y:g}h{pw}v{ph}h-{pw}z"
        for px, py, pw, ph in marks
        if px < x + w and px + pw > x and py < y + h and py + ph > y
    )


def textured(source, box, marks, palette):
    x, y, w, h = box
    match = sheet.PART_RE.match(source)
    attrs, body = match.groups()
    paths = "\n".join(
        f'<path class="paper-{key}" d="{path_for(marks[key], x, y, w, h)}" />'
        for key in ("chip", "fiber", "dust", "ink", "edge")
    )
    result = (
        '<!-- GENERATED texture by scripts/texture.py (via build-themes.py). Do not edit. -->\n'
        f'<svg{attrs}>\n{body}\n'
        '<defs><style>\n'
        '/* palette:start */\n:root { ' + palette + ' }\n/* palette:end */\n'
        '.paper-chip { fill: var(--bg); }\n'
        '.paper-fiber { fill: var(--faint); }\n'
        '.paper-dust, .paper-edge { fill: var(--muted); }\n'
        '.paper-ink { fill: var(--ink); }\n'
        '@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }\n'
        '</style></defs>\n'
        f'<g shape-rendering="crispEdges">{paths}</g>\n</svg>\n'
    )
    ET.fromstring(result)
    return result


def page_boxes(profile, cells):
    """Locate slices on the continuous sheet, including centered partial rows."""
    _, _, width, height = sheet._viewbox(profile)
    boxes = {"profile.svg": (0, 0, width, height)}
    x, y, row_h = 0, height, 0
    for cell in cells:
        name = cell["out"]
        if name in boxes:
            raise ValueError(f"texture: duplicate slice name {name}")
        boxes[name] = (x, y, cell["w"], cell["h"])
        x += cell["w"]
        row_h = max(row_h, cell["h"])
        if abs(x - width) < 0.01:
            x, y, row_h = 0, y + row_h, 0
        elif x > width:
            raise ValueError("texture: slice row exceeds page width")
    if x != 0:
        raise ValueError("texture: incomplete slice row")
    return boxes, y


def build(profiles, slices, cells, read_light, read_dark):
    """Return textured final assets for both themes, without changing sources."""
    boxes, height = page_boxes(profiles["light"], cells)
    marks = texture(height)
    output = {}
    for theme, read in (("light", read_light), ("dark", read_dark)):
        if sheet._viewbox(profiles[theme]) != sheet._viewbox(profiles["light"]):
            raise ValueError("texture: theme dimensions differ")
        # Transparent parts omit some roles. Supply all texture colors from the
        # source palettes, so fillers and the footer never use an SVG default.
        palette = {}
        for part in ("Hero-Banner.svg", "bento-bottom.svg", "btn-email.svg"):
            palette.update(re.findall(r'--([\w-]+):\s*(#[\da-fA-F]+);', read(part)))
        missing = {"bg", "ink", "faint", "muted"} - palette.keys()
        if missing:
            raise ValueError(f"texture: missing palette roles {sorted(missing)}")
        declarations = " ".join(f"--{key}: {value};" for key, value in palette.items())
        sources = {"profile.svg": profiles[theme], **slices[theme]}
        output[theme] = {
            name: textured(sources[name], box, marks, declarations)
            for name, box in boxes.items()
        }
    return output

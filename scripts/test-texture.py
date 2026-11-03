"""Layout regression checks: python3 scripts/test-texture.py."""

import unittest
from pathlib import Path
from unittest.mock import patch

import compose
import sheet
import texture

ROOT = Path(__file__).resolve().parent.parent


class TextureLayoutTests(unittest.TestCase):
    def test_positions_follow_composite_height(self):
        profile = '<svg viewBox="0 0 1000 47"></svg>'
        cells = [dict(out="left", w=400, h=10), dict(out="right", w=600, h=10),
                 dict(out="footer", w=1000, h=20)]
        boxes, height = texture.page_boxes(profile, cells)
        self.assertEqual(boxes["right"], (400, 47, 600, 10))
        self.assertEqual(boxes["footer"], (0, 57, 1000, 20))
        self.assertEqual(height, 77)

    def test_mark_crossing_fractional_join_is_present_on_both_sides(self):
        marks = [(225, 5, 3, 1)]
        self.assertEqual(texture.path_for(marks, 0, 0, 226.4, 10), "M225,5h3v1h-3z")
        self.assertEqual(texture.path_for(marks, 226.4, 0, 182.4, 10), "M-1.4,5h3v1h-3z")

    def test_project_layouts_keep_fillers_distinct_and_rows_complete(self):
        bp = sheet._projects()
        actual_read = lambda name: (ROOT / "assets" / name).read_text()
        profile = compose.compose(actual_read)
        for count in (1, 2, 3, 4, 5, 7, 8):
            with self.subTest(project_count=count):
                projects = [dict(name=f"Test {i}", link="", description="Example", lines=["Example"], tags=[])
                            for i in range(count)]
                cols, rows = bp.layout(projects)
                height = bp.card_height(projects, bp.GRIDS[cols])
                cards = {}
                for row in rows:
                    for index, (project, kind) in enumerate(row):
                        cards[f"project-{bp.slug(project['name'])}.svg"] = bp.card_svg(project, kind, height, index, cols)
                read = lambda name: cards[name] if name in cards else actual_read(name)
                with patch.object(sheet, "_projects", return_value=bp), patch.object(bp, "parse", return_value=(None, projects)):
                    cells = sheet.plan(read)
                boxes, total_height = texture.page_boxes(profile, cells)
                fillers = [c for c in cells if c["part"] is None]
                self.assertEqual(len(boxes), len(cells) + 1)
                if count % cols:
                    self.assertEqual(len(fillers), 2)
                    left, right = [boxes[c["out"]] for c in fillers]
                    self.assertEqual(left[0], 0)
                    self.assertAlmostEqual(right[0] + right[2], 1000)
                self.assertEqual(boxes["sheet-footer.svg"][1] + sheet.FOOTER_H, total_height)


if __name__ == "__main__":
    unittest.main()

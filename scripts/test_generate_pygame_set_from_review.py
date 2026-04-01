import json
import subprocess
import sys
import unittest
import uuid
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_MD = ROOT / "practice" / "data" / "content" / "pygame" / "week01" / "problem_review_round01.md"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class GeneratePygameSetFromReviewTests(unittest.TestCase):
    def make_output_path(self) -> Path:
        tmp_dir = ROOT / "practice" / "temp" / "test_outputs"
        tmp_dir.mkdir(parents=True, exist_ok=True)
        return tmp_dir / f"pygame_review_{uuid.uuid4().hex}.json"

    def run_generator(self, output_path: Path):
        subprocess.run(
            [
                sys.executable,
                "scripts/generate_pygame_set_from_review.py",
                "--source",
                str(SOURCE_MD),
                "--output",
                str(output_path),
                "--set-id",
                "py_pygame_w01_b01",
                "--title",
                "Python Pygame 1주차",
                "--category-id",
                "py_pygame_w01",
            ],
            cwd=ROOT,
            check=True,
        )

    def test_generates_section_based_set_json(self):
        output_path = self.make_output_path()
        self.run_generator(output_path)
        payload = load_json(output_path)

        self.assertEqual(payload["id"], "py_pygame_w01_b01")
        self.assertEqual(payload["categoryId"], "py_pygame_w01")
        self.assertEqual(payload["availableLanguages"], ["python"])
        self.assertEqual(len(payload["sections"]), 6)

        first_section = payload["sections"][0]
        self.assertEqual(first_section["id"], "s1")
        self.assertEqual(first_section["title"], "1번 창 생성과 화면 색")
        self.assertIn("pygame.init()", first_section["code"])
        self.assertEqual(
            first_section["media"][0]["path"],
            "../content/pygame/week01/reference_images/problem01_correct.png",
        )
        self.assertEqual(len(first_section["children"]), 4)

    def test_generates_expected_answer_shapes(self):
        output_path = self.make_output_path()
        self.run_generator(output_path)
        payload = load_json(output_path)

        first_section = payload["sections"][0]
        code_q = first_section["children"][0]
        blank_q = first_section["children"][2]
        multi_q = first_section["children"][3]

        self.assertEqual(code_q["type"], "code")
        self.assertEqual(code_q["level"], "basic")
        self.assertEqual(code_q["expectedCode"], "SURFACE.fill((255, 255, 255))")

        self.assertEqual(blank_q["type"], "short")
        self.assertEqual(blank_q["expectedText"], "400, 300")

        self.assertEqual(multi_q["type"], "mcq_multi")
        self.assertEqual(multi_q["correctIndexes"], [0, 1])
        self.assertEqual(multi_q["optionLabels"], ["A", "B", "C", "D"])
        self.assertEqual(multi_q["minSelections"], 2)
        self.assertEqual(multi_q["maxSelections"], 2)


if __name__ == "__main__":
    unittest.main()

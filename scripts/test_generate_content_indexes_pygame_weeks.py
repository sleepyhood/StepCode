import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT / "practice" / "data"
GENERATED_ROOT = DATA_ROOT / "generated"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class GenerateContentIndexesPygameWeeksTests(unittest.TestCase):
    def test_generator_emits_ten_weekly_pygame_categories(self):
        subprocess.run(
            [sys.executable, "scripts/generate_content_indexes.py"],
            cwd=ROOT,
            check=True,
        )

        categories = load_json(GENERATED_ROOT / "categories.json")
        pygame_categories = [item for item in categories if item.get("track") == "pygame"]
        pygame_ids = [item.get("id") for item in pygame_categories]

        self.assertEqual(
            pygame_ids,
            [
                "py_pygame_w01",
                "py_pygame_w02",
                "py_pygame_w03",
                "py_pygame_w04",
                "py_pygame_w05",
                "py_pygame_w06",
                "py_pygame_w07",
                "py_pygame_w08",
                "py_pygame_w09",
                "py_pygame_w10",
            ],
        )

    def test_generator_emits_weekly_pygame_theory_entries(self):
        subprocess.run(
            [sys.executable, "scripts/generate_content_indexes.py"],
            cwd=ROOT,
            check=True,
        )

        theory_index = load_json(GENERATED_ROOT / "theory.index.json")
        pygame_entries = [item for item in theory_index if item.get("track") == "pygame"]
        pygame_concept_ids = [item.get("conceptId") for item in pygame_entries]

        self.assertEqual(
            pygame_concept_ids,
            [
                "py_pygame_w01_intro",
                "py_pygame_w02_intro",
                "py_pygame_w03_intro",
                "py_pygame_w04_intro",
                "py_pygame_w05_intro",
                "py_pygame_w06_intro",
                "py_pygame_w07_intro",
                "py_pygame_w08_intro",
                "py_pygame_w09_intro",
                "py_pygame_w10_intro",
            ],
        )

    def test_generator_emits_active_week07_to_week10_interactive_entries(self):
        subprocess.run(
            [sys.executable, "scripts/generate_content_indexes.py"],
            cwd=ROOT,
            check=True,
        )

        interactive_index = load_json(GENERATED_ROOT / "interactive.index.json")
        pygame_week_entries = [
            item
            for item in interactive_index
            if item.get("id") in {
                "py_pygame_w07_b01",
                "py_pygame_w08_b01",
                "py_pygame_w09_b01",
                "py_pygame_w10_b01",
            }
        ]

        self.assertEqual(
            [item["id"] for item in pygame_week_entries],
            [
                "py_pygame_w07_b01",
                "py_pygame_w08_b01",
                "py_pygame_w09_b01",
                "py_pygame_w10_b01",
            ],
        )
        self.assertTrue(all(item.get("status") == "active" for item in pygame_week_entries))


if __name__ == "__main__":
    unittest.main()

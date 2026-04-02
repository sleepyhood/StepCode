import json
import subprocess
import sys
import unittest
import uuid
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REVIEW_DIR = ROOT / "practice" / "data" / "content" / "language" / "python" / "lv07_for" / "problem_review"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class GenerateLanguageSetFromReviewTests(unittest.TestCase):
    def make_output_path(self) -> Path:
        tmp_dir = ROOT / "practice" / "temp" / "test_outputs"
        tmp_dir.mkdir(parents=True, exist_ok=True)
        return tmp_dir / f"language_review_{uuid.uuid4().hex}.json"

    def run_generator(self, source: Path, output: Path, set_id: str, title: str, round_no: int, difficulty: str):
        subprocess.run(
            [
                sys.executable,
                "scripts/generate_language_set_from_review.py",
                "--source",
                str(source),
                "--output",
                str(output),
                "--set-id",
                set_id,
                "--title",
                title,
                "--category-id",
                "py_for",
                "--round",
                str(round_no),
                "--difficulty",
                difficulty,
            ],
            cwd=ROOT,
            check=True,
        )

    def test_generates_basic_round_json(self):
        source = REVIEW_DIR / "problem_review_basic_r01.md"
        output = self.make_output_path()
        self.run_generator(
            source=source,
            output=output,
            set_id="py_lv07_for_b01",
            title="Python for문 기초 1회차",
            round_no=1,
            difficulty="basic",
        )
        payload = load_json(output)
        self.assertEqual(payload["id"], "py_lv07_for_b01")
        self.assertEqual(payload["categoryId"], "py_for")
        self.assertEqual(payload["availableLanguages"], ["python"])
        self.assertEqual(len(payload["problems"]), 5)
        self.assertIn("expectedGrid", payload["problems"][0])
        self.assertIn("expectedCode", payload["problems"][-1])

    def test_generates_challenge_round_json(self):
        source = REVIEW_DIR / "problem_review_challenge_r02.md"
        output = self.make_output_path()
        self.run_generator(
            source=source,
            output=output,
            set_id="py_lv07_for_c01",
            title="Python for문 챌린지 1회차",
            round_no=2,
            difficulty="challenge",
        )
        payload = load_json(output)
        self.assertEqual(payload["id"], "py_lv07_for_c01")
        self.assertEqual(len(payload["problems"]), 6)
        self.assertEqual(payload["problems"][0]["level"], "챌린지")
        self.assertIn("ioExample", payload["problems"][0])


if __name__ == "__main__":
    unittest.main()

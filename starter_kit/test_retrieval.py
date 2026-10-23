import json
import unittest
from pathlib import Path

from retrieval import answer_question, load_docs


DATA_DIR = Path(__file__).parent / "data"


class RetrievalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.docs = load_docs(DATA_DIR / "docs.json")
        with open(DATA_DIR / "example_questions.json", encoding="utf-8") as file:
            cls.questions = json.load(file)["example_questions"]

    def test_expected_docs_and_abstention(self):
        for item in self.questions:
            with self.subTest(question=item["question_id"]):
                result = answer_question(item["question"], self.docs)
                if item["expected_doc_id"] is None:
                    self.assertFalse(result["answered"])
                else:
                    self.assertTrue(result["answered"])
                    self.assertEqual(result["source"]["doc_id"], item["expected_doc_id"])

    def test_answers_include_requested_facts(self):
        expected_facts = {
            "Q-2": "15 minutes",
            "Q-3": "10,000 rows",
            "Q-4": "60 requests per minute",
        }
        for item in self.questions:
            if item["question_id"] in expected_facts:
                with self.subTest(question=item["question_id"]):
                    result = answer_question(item["question"], self.docs)
                    self.assertIn(expected_facts[item["question_id"]], result["answer"])


if __name__ == "__main__":
    unittest.main()
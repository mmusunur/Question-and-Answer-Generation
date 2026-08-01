"""
Automated Unit Test Suite for Question-and-Answer-Generation Engine.
"""

import unittest
import os
import json
import csv
from quest import parse as parse_factual, gen_ne_questions
from blanks import generate_blanks_questions, get_wordnet_distractors
from mcqs import sample_quiz, QA
from exporter import export_questions


class TestQuestionGeneration(unittest.TestCase):

    def test_factual_question_generation(self):
        sample_text = "Bansoori is an Indian classical instrument. Akhil plays Bansoori."
        questions = parse_factual(sample_text)
        self.assertIsInstance(questions, list)
        self.assertGreaterEqual(len(questions), 1)

    def test_named_entity_who_questions(self):
        sample_text = "Akhil visited Minsk in Belarus."
        ne_qs = gen_ne_questions(sample_text)
        self.assertTrue(any("Who" in q[0] or "Where" in q[0] for q in ne_qs))

    def test_blanks_generation_with_smart_distractors(self):
        text = "Osmosis is the movement of a solvent across a semipermeable membrane."
        questions_data = generate_blanks_questions(text)
        self.assertIsInstance(questions_data, list)
        if len(questions_data) > 0:
            q_text, choices, answer = questions_data[0]
            self.assertIn("__________________", q_text)
            self.assertEqual(len(choices), 4)
            self.assertIn(answer, choices)

    def test_wordnet_distractors(self):
        distractors = get_wordnet_distractors("water", pos_tag='n', max_count=3)
        self.assertIsInstance(distractors, list)

    def test_mcq_quiz_structure(self):
        quiz = sample_quiz()
        self.assertGreater(len(quiz), 0)
        first_item = quiz[0]
        self.assertIsInstance(first_item, QA)

    def test_json_export(self):
        output_file = "test_export.json"
        if os.path.exists(output_file):
            os.remove(output_file)

        sample_text = "Priya writes poems. Osmosis is the movement of water."
        count = export_questions(sample_text, output_file, file_format="json")
        self.assertGreater(count, 0)
        self.assertTrue(os.path.exists(output_file))

        with open(output_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertEqual(len(data), count)

        if os.path.exists(output_file):
            os.remove(output_file)

    def test_csv_export(self):
        output_file = "test_export.csv"
        if os.path.exists(output_file):
            os.remove(output_file)

        sample_text = "Priya writes poems. Osmosis is the movement of water."
        count = export_questions(sample_text, output_file, file_format="csv")
        self.assertGreater(count, 0)
        self.assertTrue(os.path.exists(output_file))

        with open(output_file, "r", encoding="utf-8") as f:
            reader = list(csv.reader(f))
            self.assertEqual(len(reader), count + 1)  # Header + rows

        if os.path.exists(output_file):
            os.remove(output_file)


if __name__ == "__main__":
    unittest.main()

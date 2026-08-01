"""
Automated Unit Test Suite for Question-and-Answer-Generation Engine & LLM Package.
"""

import unittest
import os
import json
import csv
from qg_engine import QuestionGenerator, LLMProvider, DocChatbot, export_questions
from quest import parse as parse_factual, gen_ne_questions
from blanks import generate_blanks_questions, get_wordnet_distractors
from mcqs import sample_quiz, QA


class TestQuestionGeneration(unittest.TestCase):

    def test_reusable_question_generator_nlp(self):
        qg = QuestionGenerator(mode="nlp")
        text = "Akhil plays Bansoori. Osmosis is the movement of water."
        factual_qs = qg.generate_factual_questions(text)
        self.assertIsInstance(factual_qs, list)
        self.assertGreaterEqual(len(factual_qs), 1)

        mcq_qs = qg.generate_fill_in_blanks(text)
        self.assertIsInstance(mcq_qs, list)
        self.assertGreaterEqual(len(mcq_qs), 1)

    def test_llm_provider_availability(self):
        llm = LLMProvider()
        # When no API key is set, is_available returns False cleanly
        self.assertIsInstance(llm.is_available(), bool)

    def test_doc_chatbot_fallback(self):
        doc_text = "Osmosis is the movement of water. Raja-Yoga has eight steps."
        bot = DocChatbot(doc_text)
        reply = bot.chat("What is osmosis?")
        self.assertIsInstance(reply, str)
        self.assertIn("osmosis", reply.lower())

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
            self.assertEqual(len(reader), count + 1)

        if os.path.exists(output_file):
            os.remove(output_file)


if __name__ == "__main__":
    unittest.main()

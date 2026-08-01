"""
Automated Unit Test Suite for Question-and-Answer-Generation.
"""

import unittest
from quest import parse, genQuestion
from blanks import generate_blanks_questions
from mcqs import sample_quiz, QA


class TestQuestionGeneration(unittest.TestCase):

    def test_factual_question_generation(self):
        sample_text = "Bansoori is an Indian classical instrument. Akhil plays Bansoori."
        questions = parse(sample_text)
        self.assertIsInstance(questions, list)
        self.assertGreaterEqual(len(questions), 1)
        self.assertTrue(any("Bansoori" in q for q in questions))

    def test_single_sentence_gen_question(self):
        sentence = "Priya writes poems."
        q = genQuestion(sentence)
        self.assertTrue(q.startswith("What"))

    def test_blanks_generation(self):
        text = "Osmosis is the movement of a solvent across a semipermeable membrane toward a higher concentration of solute."
        questions_data = generate_blanks_questions(text)
        self.assertIsInstance(questions_data, list)
        if len(questions_data) > 0:
            q_text, choices, answer = questions_data[0]
            self.assertIn("__________________", q_text)
            self.assertEqual(len(choices), 4)
            self.assertIn(answer, choices)

    def test_mcq_quiz_structure(self):
        quiz = sample_quiz()
        self.assertGreater(len(quiz), 0)
        first_item = quiz[0]
        self.assertIsInstance(first_item, QA)
        self.assertIsNotNone(first_item.question)
        self.assertIsNotNone(first_item.corr_answ)


if __name__ == "__main__":
    unittest.main()

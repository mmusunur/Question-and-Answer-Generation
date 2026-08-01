"""
Core Hybrid Question Generator Component.
Provides a unified interface for generating questions using either local NLP rules or LLM providers.
"""

from quest import parse as parse_factual
from blanks import generate_blanks_questions
from .llm_provider import LLMProvider
from .exporter import export_questions


class QuestionGenerator:
    """
    Reusable Question Generator Component.
    
    Example Usage:
        qg = QuestionGenerator()
        factual_qs = qg.generate_factual_questions("Priya writes poems.")
        mcq_qs = qg.generate_fill_in_blanks("Osmosis is the movement of water.")
    """
    def __init__(self, mode="auto", api_key=None, provider=None):
        self.mode = mode.lower()
        self.llm = LLMProvider(api_key=api_key, provider=provider)

    def generate_factual_questions(self, text):
        """Generates factual questions (What, Who, Where, When)."""
        if self.mode == "llm" or (self.mode == "auto" and self.llm.is_available()):
            try:
                qa_data = self.llm.generate_json_qa(text, count=5)
                return [q["question"] for q in qa_data if q.get("question")]
            except Exception:
                pass

        # Local NLP fallback
        return parse_factual(text)

    def generate_fill_in_blanks(self, text):
        """Generates fill-in-the-blank questions with 4 multiple choice options."""
        if self.mode == "llm" or (self.mode == "auto" and self.llm.is_available()):
            try:
                qa_data = self.llm.generate_json_qa(text, count=5)
                results = []
                for item in qa_data:
                    if item.get("options") and len(item["options"]) == 4:
                        results.append((item["question"], item["options"], item.get("answer", "")))
                if results:
                    return results
            except Exception:
                pass

        # Local NLP fallback
        return generate_blanks_questions(text)

    def export(self, text, output_path, file_format="json"):
        """Exports questions to JSON or CSV format."""
        return export_questions(text, output_path, file_format=file_format)

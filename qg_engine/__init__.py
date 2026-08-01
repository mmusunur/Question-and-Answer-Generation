"""
Question & Answer Generation Engine (QG Engine).
A reusable Python framework for NLP-based and LLM-powered question generation, MCQ creation, and document chat.
"""

from .core import QuestionGenerator
from .llm_provider import LLMProvider
from .chatbot import DocChatbot
from .exporter import export_questions

__all__ = [
    "QuestionGenerator",
    "LLMProvider",
    "DocChatbot",
    "export_questions",
]

"""
Document Chatbot Engine.
Allows conversing with an input document, answering user queries, and asking custom questions.
"""

import re
from textblob import TextBlob
from .llm_provider import LLMProvider
from .core import QuestionGenerator


class DocChatbot:
    def __init__(self, document_text, api_key=None, provider=None):
        self.doc_text = document_text
        self.llm = LLMProvider(api_key=api_key, provider=provider)
        self.qg = QuestionGenerator(api_key=api_key)
        self.chat_history = []

    def chat(self, user_query):
        """Processes user question about document using LLM or fallback NLP search."""
        if self.llm.is_available():
            system_prompt = (
                "You are an intelligent document assistant. Answer the user's questions based strictly "
                "on the provided document context. Be concise, accurate, and helpful.\n\n"
                f"DOCUMENT CONTEXT:\n{self.doc_text}"
            )
            reply = self.llm.generate_text(user_query, system_instruction=system_prompt)
            self.chat_history.append({"user": user_query, "bot": reply})
            return reply
        else:
            # Fallback robust sentence matching using TextBlob
            blob = TextBlob(self.doc_text)
            sentences = [str(s).strip() for s in blob.sentences if str(s).strip()]
            keywords = [w.lower().strip("?,.!") for w in user_query.split() if len(w) > 2 and w.lower() not in ['what', 'where', 'when', 'who', 'how', 'is', 'are', 'the']]
            
            matches = []
            for s in sentences:
                s_lower = s.lower()
                score = sum(1 for kw in keywords if kw in s_lower)
                if score > 0:
                    matches.append((score, s))

            matches.sort(key=lambda x: x[0], reverse=True)
            if matches:
                reply = f"[NLP Fallback Answer]: " + " ".join([m[1] for m in matches[:2]])
            else:
                reply = "[NLP Fallback Answer]: I couldn't find a direct match in the document for your question."

            self.chat_history.append({"user": user_query, "bot": reply})
            return reply

    def start_interactive_session(self):
        """Runs an interactive terminal chat session with the document."""
        print("\n" + "=" * 60)
        print("         DOCUMENT CHATBOT ASSISTANT")
        print("  Ask questions about the text or type 'quiz' to take a quiz!")
        print("  Type 'exit' or 'quit' to end the session.")
        print("=" * 60 + "\n")

        while True:
            try:
                user_input = input("You: ").strip()
                if not user_input:
                    continue
                if user_input.lower() in ['exit', 'quit', 'q']:
                    print("Ending chatbot session. Goodbye!")
                    break
                elif user_input.lower() == 'quiz':
                    print("\nGenerating Quiz from Document...\n")
                    questions = self.qg.generate_fill_in_blanks(self.doc_text)
                    for idx, (q, choices, ans) in enumerate(questions, 1):
                        print(f"Q{idx}: {q}")
                        for c_idx, c in enumerate(choices, 1):
                            print(f"  {c_idx}. {c}")
                        print(f"Answer: {ans}\n")
                    continue

                reply = self.chat(user_input)
                print(f"\nBot: {reply}\n")
            except (KeyboardInterrupt, EOFError):
                print("\nEnding chatbot session.")
                break

"""
LLM Provider Integration.
Supports Google Gemini, OpenAI, and custom OpenAI-compatible REST endpoints.
"""

import os
import json
import requests


class LLMProvider:
    def __init__(self, api_key=None, provider=None, model=None):
        self.api_key = (
            api_key or 
            os.getenv("GEMINI_API_KEY") or 
            os.getenv("OPENAI_API_KEY") or 
            os.getenv("LLM_API_KEY")
        )
        
        # Determine provider
        if provider:
            self.provider = provider.lower()
        elif os.getenv("GEMINI_API_KEY"):
            self.provider = "gemini"
        elif os.getenv("OPENAI_API_KEY"):
            self.provider = "openai"
        else:
            self.provider = "gemini" if self.api_key else None

        self.model = model or ("gemini-1.5-flash" if self.provider == "gemini" else "gpt-3.5-turbo")

    def is_available(self):
        """Returns True if an LLM API key is configured."""
        return bool(self.api_key)

    def generate_text(self, prompt, system_instruction=None):
        """Sends a text generation query to the configured LLM API."""
        if not self.is_available():
            raise ValueError("No LLM API Key set. Please set GEMINI_API_KEY or OPENAI_API_KEY environment variable.")

        if self.provider == "gemini":
            return self._call_gemini(prompt, system_instruction)
        elif self.provider == "openai":
            return self._call_openai(prompt, system_instruction)
        else:
            raise ValueError(f"Unsupported LLM provider '{self.provider}'")

    def _call_gemini(self, prompt, system_instruction=None):
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        headers = {"Content-Type": "application/json"}
        
        contents = []
        if system_instruction:
            contents.append({"role": "user", "parts": [{"text": f"System Instruction: {system_instruction}"}]})
            contents.append({"role": "model", "parts": [{"text": "Understood. I will follow your instructions."}]})
        
        contents.append({"role": "user", "parts": [{"text": prompt}]})

        payload = {"contents": contents}
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()

        try:
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError) as e:
            raise RuntimeError(f"Error parsing Gemini response: {e}. Raw response: {data}")

    def _call_openai(self, prompt, system_instruction=None):
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        messages = []
        if system_instruction:
            messages.append({"role": "system", "content": system_instruction})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.3
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()

        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as e:
            raise RuntimeError(f"Error parsing OpenAI response: {e}. Raw response: {data}")

    def generate_json_qa(self, text, count=5):
        """Generates structured high-accuracy Q&A using LLM JSON output."""
        system_prompt = (
            "You are an expert NLP question generator. Extract factual questions and multiple-choice options "
            "from the provided text. Return ONLY a valid JSON array of objects, where each object has keys: "
            "'type' ('factual' or 'mcq'), 'question', 'options' (list of 4 strings for mcq, empty list for factual), "
            "'answer', and 'explanation'."
        )
        user_prompt = f"Text to process:\n\n{text}\n\nGenerate {count} high quality questions."
        
        raw_response = self.generate_text(user_prompt, system_instruction=system_prompt)
        
        # Clean JSON markdown fences if present
        clean_text = raw_response.strip()
        if clean_text.startswith("```"):
            clean_text = clean_text.split("```")[1]
            if clean_text.startswith("json"):
                clean_text = clean_text[4:]
        clean_text = clean_text.strip()

        try:
            return json.loads(clean_text)
        except json.JSONDecodeError:
            return [{"type": "raw", "question": "LLM Response", "options": [], "answer": raw_response}]

# Automatic Question and Answer Generation Engine & Chatbot

A reusable, high-accuracy Python framework and CLI tool for **NLP-based and LLM-powered** Question and Answer Generation, Fill-in-the-Blanks, Multiple-Choice Questions (MCQs), and Conversational Document Chat.

Modernized and expanded for **Python 3.10+**, **NLTK 3.9+**, **TextBlob 0.20+**, and **Google Gemini / OpenAI LLM APIs**.

---

## Key Features

- **Hybrid AI Engine (`qg_engine`)**: Uses **Google Gemini / OpenAI LLMs** when API keys are configured (`GEMINI_API_KEY`, `OPENAI_API_KEY`, `LLM_API_KEY`) for state-of-the-art accuracy, with automatic seamless fallback to local NLTK & TextBlob NLP rules when offline.
- **Conversational Document Chatbot (`DocChatbot`)**: Chat directly with any input document via terminal (`python main.py chat in.txt`) or import as a Python class.
- **Multi-Type Question Generation**: Generates **What**, **Who**, **Where**, and **When** questions.
- **WordNet Smart Distractor Generation**: Uses NLTK WordNet hypernym/hyponym semantic trees to create realistic multiple-choice options.
- **JSON & CSV Export Engine**: Export generated Q&A pairs directly to structured `.json` or `.csv` files.
- **Reusable Python Component (`qg_engine`)**: Easily import into external Python projects.

---

## Reusable Component Python API

You can import `qg_engine` into any Python project:

```python
from qg_engine import QuestionGenerator, DocChatbot

# 1. Initialize Question Generator (Auto-detects LLM API keys or uses local NLP)
qg = QuestionGenerator(mode="auto")

text = "Osmosis is the movement of a solvent across a semipermeable membrane. Priya writes poems."

# 2. Generate Factual Questions
factual_qs = qg.generate_factual_questions(text)
print(factual_qs)

# 3. Generate Fill-in-the-Blank Multiple Choice Questions
mcq_qs = qg.generate_fill_in_blanks(text)
for q, choices, answer in mcq_qs:
    print(f"Q: {q}\nChoices: {choices}\nAnswer: {answer}\n")

# 4. Document Chatbot
bot = DocChatbot(text)
reply = bot.chat("What is osmosis?")
print("Bot Reply:", reply)
```

---

## Unified Command Line Interface (`main.py`)

### 1. Document Chatbot Assistant (`chat`)

Start an interactive AI chatbot session to query any text file:

```bash
python main.py chat in.txt
```

### 2. Generate Factual Questions (`quest`)

```bash
python main.py quest in.txt
```

### 3. Generate Fill-in-the-Blanks Questions (`blanks`)

```bash
python main.py blanks in.txt
```

### 4. Run Interactive MCQ Quiz (`quiz`)

```bash
python main.py quiz
```

### 5. Export Questions to JSON or CSV (`export`)

```bash
# Export to JSON
python main.py export in.txt --format json --output questions.json

# Export to CSV
python main.py export in.txt --format csv --output questions.csv
```

---

## LLM Configuration (Optional for High Accuracy)

To enable LLM-backed question generation and chatbot responses, set your API key in your environment:

```bash
# Google Gemini
set GEMINI_API_KEY=your_gemini_api_key_here

# OpenAI
set OPENAI_API_KEY=your_openai_api_key_here
```

If no key is set, the system automatically runs the local NLP engine.

---

## Automated Unit Testing

Run the unit test suite:

```bash
python -m unittest test_qg.py
```

---

## Project Structure

```
Question-and-Answer-Generation/
├── qg_engine/                 # Reusable Python Package
│   ├── __init__.py            # Exports QuestionGenerator, LLMProvider, DocChatbot, export_questions
│   ├── core.py                # Main QuestionGenerator class (Hybrid LLM + Rule NLP)
│   ├── llm_provider.py        # Google Gemini & OpenAI LLM REST integration
│   ├── chatbot.py            # Conversational Document Chatbot engine
│   └── exporter.py            # JSON / CSV Exporter module
├── main.py                    # Unified CLI (quest, blanks, quiz, chat, export)
├── quest.py                   # Factual question generator wrapper
├── blanks.py                  # Fill-in-the-blanks generator wrapper
├── mcqs.py                    # Interactive MCQ quiz runner
├── test_qg.py                 # Automated unit test suite
├── requirements.txt           # Python dependencies
├── .gitignore
├── README.md                  # Project documentation
├── in.txt                     # Short text input sample
└── test.txt                   # Evaluation text file
```

---

## License & Attribution

Originally created by Indrajith Indraprastham (2017). Refactored, modernized, and expanded with hybrid LLM capabilities and reusable component architecture.

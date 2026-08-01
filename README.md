# Automatic Question and Answer Generation Engine

An advanced NLP-powered Question and Answer Generation Engine that generates **Factual Questions** (What, Who, Where, When), **Fill-in-the-Blanks**, and **Multiple-Choice Questions (MCQs)** with smart distractor generation using **TextBlob**, **NLTK**, and **WordNet**.

Updated, modernized, and expanded for **Python 3.10+**, **NLTK 3.9+**, and **TextBlob 0.20+**.

---

## Highlights & Performance Enhancements

- **Multi-Type Question Generation**: Generates **What**, **Who**, **Where**, and **When** questions using Named Entity Recognition (NER) and syntactic Part-of-Speech (POS) parsing.
- **Smart Distractor Generation**: Uses **NLTK WordNet** hyponym/hypernym semantic trees and same-POS candidate matching to generate realistic multiple-choice options.
- **Unified CLI (`main.py`)**: Run any engine capability (`quest`, `blanks`, `quiz`, `export`) from a single command line interface.
- **JSON & CSV Export (`exporter.py`)**: Export generated question & answer pairs to structured `JSON` or `CSV` files for LMS integration, flashcard apps (Anki), or downstream NLP pipelines.
- **100% Automated Test Coverage (`test_qg.py`)**: Fully verified unit test suite.

---

## Installation & Setup

### 1. Prerequisites

Python 3.10 or higher is required.

```bash
python --version
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Unified Command Line Interface (`main.py`)

### 1. Generate Factual Questions (`quest`)

Generates What, Who, Where, and When questions:

```bash
python main.py quest in.txt
```

### 2. Generate Fill-in-the-Blanks Questions (`blanks`)

Generates fill-in-the-blanks with 4 multiple-choice options powered by WordNet smart distractors:

```bash
python main.py blanks in.txt
```

### 3. Run Interactive MCQ Quiz (`quiz`)

Launch an interactive terminal quiz session:

```bash
python main.py quiz
```

### 4. Export Questions to JSON or CSV (`export`)

Export questions directly to structured JSON or CSV:

```bash
# Export to JSON
python main.py export in.txt --format json --output questions.json

# Export to CSV
python main.py export in.txt --format csv --output questions.csv
```

---

## Automated Unit Testing

Run the comprehensive unit test suite:

```bash
python -m unittest test_qg.py
```

---

## Project Structure

```
Question-and-Answer-Generation/
├── main.py                # Unified CLI entrypoint (quest, blanks, quiz, export)
├── quest.py               # Advanced multi-type question generator (What, Who, Where, When)
├── blanks.py              # Fill-in-the-blanks generator with WordNet smart distractors
├── mcqs.py                # Interactive MCQ quiz runner
├── exporter.py            # JSON and CSV export engine
├── test_qg.py             # Automated unit test suite
├── requirements.txt       # Updated Python dependencies
├── .gitignore             # Git ignore configuration
├── README.md              # Project documentation
├── in.txt                 # Short text input sample
└── test.txt               # Evaluation text file
```

---

## License & Attribution

Originally created by Indrajith Indraprastham (2017). Enhanced, modernized, and expanded for modern Python and NLP pipelines.

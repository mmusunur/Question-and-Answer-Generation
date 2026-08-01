# Automatic Question and Answer Generation

This repository generates questions (Factual Questions, Fill-in-the-Blanks, and Multiple-Choice Questions) from input text using Natural Language Processing (NLP) with **TextBlob** and **NLTK**.

Updated and modernized for Python **3.10+**, **NLTK 3.9+**, and **TextBlob 0.20+**.

---

## Features

- **Factual Question Generation (`quest.py`)**: Generates "What" questions based on Part-of-Speech (POS) grammar patterns.
- **Fill-in-the-Blanks Generator (`blanks.py` & `blanks1.py`)**: Replaces proper nouns or common nouns with blanks and creates distractor options for multiple-choice quizzes.
- **Interactive MCQ Quiz System (`mcqs.py`)**: Runs an interactive terminal-based quiz.
- **Named Entity Chunker (`gen.py`)**: Analyzes named entity syntax trees using NLTK.
- **Automated Test Suite (`test_qg.py`)**: Unit tests covering question generation, fill-in-the-blanks, and MCQ generation.

---

## Installation & Setup

### 1. Prerequisites

Python 3.10 or higher is recommended.

```bash
python --version
```

### 2. Install Dependencies

Install the modern required packages:

```bash
pip install -r requirements.txt
```

---

## Quick Start & Usage

### 1. Generate Factual Questions (`quest.py`)

Run on any input text file:

```bash
python quest.py in.txt
```

To enable verbose mode (displays POS tags and rule matching info):

```bash
python quest.py in.txt -v
```

### 2. Generate Fill-in-the-Blanks Questions (`blanks.py`)

```bash
python blanks.py file1.txt
```

### 3. Run Interactive MCQ Quiz (`mcqs.py`)

```bash
python mcqs.py
```

### 4. Run Automated Unit Tests

```bash
python -m unittest test_qg.py
```

---

## Penn Treebank POS Tags Reference

| Tag | Description |
|---|---|
| `NNP` | Proper noun, singular |
| `NN` | Noun, singular or mass |
| `NNS` | Noun, plural |
| `VBZ` | Verb, 3rd person singular present |
| `VBG` | Verb, gerund or present participle |
| `VBD` | Verb, past tense |
| `VBN` | Verb, past participle |
| `JJ` | Adjective |
| `IN` | Preposition or subordinating conjunction |
| `PRP` | Personal pronoun |

---

## Project Structure

```
Question-and-Answer-Generation/
├── quest.py               # Factual question generator (Main module)
├── blanks.py              # Fill-in-the-blank question & options generator
├── blanks1.py             # Simple fill-in-the-blank text generator
├── mcqs.py                # Interactive MCQ quiz runner
├── gen.py                 # NLTK Named Entity syntax tree parser
├── sample.py              # Probability-based question answer scoring
├── example.py             # TextBlob POS tag analysis example
├── test_qg.py             # Automated unit tests
├── requirements.txt       # Updated Python package dependencies
├── .gitignore             # Git ignore configuration
├── README.md              # Project documentation
├── report.md              # Project report
├── in.txt                 # Sample text input file
├── file1.txt              # Sample input text file 1
├── file2.txt              # Sample input text file 2
├── file3.txt              # Sample input text file 3
└── test.txt               # Sample evaluation text file
```

---

## License & Attribution

Originally created by Indrajith Indraprastham (2017). Modernized and refactored for current Python and NLP libraries.

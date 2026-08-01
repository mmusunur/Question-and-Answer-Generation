"""
Question Generation System from Text using Part-of-Speech Tagging and Rule-Based Parsing.
"""

import sys
import nltk
from textblob import TextBlob, Word

verbose = False


def ensure_nltk_data():
    """Ensure required NLTK data packages are downloaded."""
    packages = [
        'punkt',
        'punkt_tab',
        'averaged_perceptron_tagger',
        'averaged_perceptron_tagger_eng',
        'brown',
    ]
    for pkg in packages:
        try:
            nltk.download(pkg, quiet=True)
        except Exception:
            pass


def genQuestion(line):
    """
    Generates a question from a given sentence (TextBlob or string object).
    Returns the generated question string or empty string if no rule matches.
    """
    if isinstance(line, str):
        line = TextBlob(line)

    bucket = {}
    for i, (word, tag) in enumerate(line.tags):
        if tag not in bucket:
            bucket[tag] = i

    question = ''

    # Rule tag combinations
    l1 = ['NNP', 'VBG', 'VBZ', 'IN']
    l2 = ['NNP', 'VBG', 'VBZ']
    l3 = ['PRP', 'VBG', 'VBZ', 'IN']
    l4 = ['PRP', 'VBG', 'VBZ']
    l5 = ['PRP', 'VBG', 'VBD']
    l6 = ['NNP', 'VBG', 'VBD']
    l7 = ['NN', 'VBG', 'VBZ']
    l8 = ['NNP', 'VBZ', 'JJ']
    l9 = ['NNP', 'VBZ', 'NN']
    l10 = ['NNP', 'VBZ']
    l11 = ['PRP', 'VBZ']
    l12 = ['NNP', 'NN', 'IN']
    l13 = ['NN', 'VBZ']

    if all(key in bucket for key in l1):
        question = f"What {line.words[bucket['VBZ']]} {line.words[bucket['NNP']]} {line.words[bucket['VBG']]}?"
    elif all(key in bucket for key in l2):
        question = f"What {line.words[bucket['VBZ']]} {line.words[bucket['NNP']]} {line.words[bucket['VBG']]}?"
    elif all(key in bucket for key in l3):
        question = f"What {line.words[bucket['VBZ']]} {line.words[bucket['PRP']]} {line.words[bucket['VBG']]}?"
    elif all(key in bucket for key in l4):
        question = f"What {line.words[bucket['PRP']]} does {line.words[bucket['VBG']]} {line.words[bucket['VBG']]}?"
    elif all(key in bucket for key in l7):
        question = f"What {line.words[bucket['VBZ']]} {line.words[bucket['NN']]} {line.words[bucket['VBG']]}?"
    elif all(key in bucket for key in l8):
        question = f"What {line.words[bucket['VBZ']]} {line.words[bucket['NNP']]}?"
    elif all(key in bucket for key in l9):
        question = f"What {line.words[bucket['VBZ']]} {line.words[bucket['NNP']]}?"
    elif all(key in bucket for key in l11):
        prp_word = line.words[bucket['PRP']].lower()
        if prp_word in ['she', 'he']:
            vbz_word = Word(line.words[bucket['VBZ']]).singularize()
            question = f"What does {prp_word} {vbz_word}?"
    elif all(key in bucket for key in l10):
        vbz_word = Word(line.words[bucket['VBZ']]).singularize()
        question = f"What does {line.words[bucket['NNP']]} {vbz_word}?"
    elif all(key in bucket for key in l13):
        question = f"What {line.words[bucket['VBZ']]} {line.words[bucket['NN']]}?"

    if 'VBZ' in bucket and line.words[bucket['VBZ']] in ["’", "'"]:
        question = question.replace(" ’ ", "'s ").replace(" ' ", "'s ")

    if question:
        print('Question: ', question)

    if verbose:
        print('Answer:', line)
        print('TAGS:', line.tags)
        print('BUCKET:', bucket)
        print('-' * 40)

    return question


def parse(string):
    """
    Parse a paragraph. Divide it into sentences and try to generate questions from each sentence.
    Returns list of generated questions.
    """
    ensure_nltk_data()
    questions = []
    txt = TextBlob(string)
    for sentence in txt.sentences:
        q = genQuestion(sentence)
        if q:
            questions.append(q)
    return questions


def main():
    global verbose
    verbose = False

    if len(sys.argv) < 2:
        print("Usage: python quest.py <filename> [-v]")
        print("Example: python quest.py in.txt -v")
        sys.exit(1)

    filepath = sys.argv[1]
    if len(sys.argv) >= 3 and sys.argv[2] == '-v':
        print('Verbose Mode Activated\n')
        verbose = True

    try:
        with open(filepath, 'r', encoding='utf-8') as filehandle:
            textinput = filehandle.read()
    except Exception as e:
        print(f"Error reading file '{filepath}': {e}")
        sys.exit(1)

    print('\n-----------INPUT TEXT-------------\n')
    print(textinput, '\n')
    print('\n-----------INPUT END---------------\n')

    parse(textinput)


if __name__ == "__main__":
    main()

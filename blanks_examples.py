"""
Fill-in-the-Blank Example Tester.
"""

import sys
import nltk
from textblob import TextBlob


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


def main():
    ensure_nltk_data()
    filename = sys.argv[1] if len(sys.argv) > 1 else 'in.txt'
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = f.read()
    except Exception as e:
        print(f"Error reading '{filename}': {e}")
        sys.exit(1)

    text = TextBlob(data)
    sentences = text.sentences
    print("SENTENCE-COUNT:", len(sentences))

    poss = {}
    for word, tag in text.tags:
        if tag not in poss:
            poss[tag] = []
        poss[tag].append(word)

    words = []
    if 'NNP' in poss:
        words = poss['NNP']
        print("Proper Nouns found (NNP):", words)
    elif 'NN' in poss:
        words = poss['NN']
        print("Common Nouns found (NN):", words)
    else:
        print("NN and NNP not found in text.")

    print("Words length:", len(words))
    if len(words) > 0:
        target = words[0]
        print("Target Blank Word:", target)


if __name__ == "__main__":
    main()
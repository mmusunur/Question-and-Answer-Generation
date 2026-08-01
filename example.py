"""
TextBlob Tag Counter & Sentence Analysis Example.
"""

import sys
from collections import Counter
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


def analyze_text(filepath):
    ensure_nltk_data()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = f.read()
    except Exception as e:
        print(f"Error opening file '{filepath}': {e}")
        return

    text = TextBlob(data)
    sentences = text.sentences
    print("Sentence Count:", len(sentences))

    tags_count = Counter(tag for word, tag in text.tags)
    print("Tags Count:", tags_count)
    print("Sentences:")
    for idx, sentence in enumerate(sentences, 1):
        print(f"  {idx}: {str(sentence)}")

    bucket = {}
    for sentence in sentences:
        for i, (word, tag) in enumerate(sentence.tags):
            if tag not in bucket:
                bucket[tag] = i

    print("Unique POS First Positions:", bucket)


def main():
    filename = sys.argv[1] if len(sys.argv) > 1 else 'file1.txt'
    analyze_text(filename)


if __name__ == "__main__":
    main()
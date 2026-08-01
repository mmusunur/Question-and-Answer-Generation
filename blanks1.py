"""
Simplified Fill-in-the-Blank Generator module.
"""

import sys
import random
import re
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


def replace_case_insensitive(word, sentence_text):
    """Replace word with blank line case-insensitively."""
    pattern = re.compile(re.escape(word), re.IGNORECASE)
    return pattern.sub('__________________', sentence_text)


def remove_word(sentence_text, pos_dict):
    """Select a proper-noun or noun to replace with blank."""
    words = None
    if 'NNP' in pos_dict and pos_dict['NNP']:
        words = pos_dict['NNP']
    elif 'NN' in pos_dict and pos_dict['NN']:
        words = pos_dict['NN']
    else:
        return (None, sentence_text, None)

    if words:
        word = random.choice(words)
        replaced = replace_case_insensitive(word, sentence_text)
        return (word, sentence_text, replaced)
    return (None, sentence_text, None)


def main():
    ensure_nltk_data()
    filename = sys.argv[1] if len(sys.argv) > 1 else 'file1.txt'

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = f.read()
    except Exception as e:
        print(f"Error reading file '{filename}': {e}")
        sys.exit(1)

    blob = TextBlob(data)
    sposs = {}

    for sentence in blob.sentences:
        sent_str = str(sentence)
        poss = {}
        for word, tag in sentence.tags:
            if tag not in poss:
                poss[tag] = []
            poss[tag].append(word)
        sposs[sent_str] = poss

    print(f"\nFill-in-the-Blank Output for '{filename}':\n")
    for sent_str, poss in sposs.items():
        word, osentence, replaced = remove_word(sent_str, poss)
        if replaced is None:
            continue
        print(replaced)
        print("Answer:", word)
        print("-" * 30)


if __name__ == "__main__":
    main()
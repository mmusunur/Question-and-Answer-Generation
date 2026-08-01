"""
Fill-in-the-Blanks Question Generator
Generates fill-in-the-blank questions with multiple-choice distractor options from text input.
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
    """
    Selects a target noun (proper noun NNP prioritized over common noun NN)
    to replace with a blank line.
    """
    words = None
    if 'NNP' in pos_dict and pos_dict['NNP']:
        words = pos_dict['NNP']
    elif 'NN' in pos_dict and pos_dict['NN']:
        words = pos_dict['NN']
    else:
        return (None, sentence_text, None)

    if words:
        target_word = words[0]
        words_sample = words[:4]
        replaced_text = replace_case_insensitive(target_word, sentence_text)
        return (words_sample, sentence_text, replaced_text)
    return (None, sentence_text, None)


def generate_blanks_questions(text):
    """
    Given an input text string, parses sentences and generates fill-in-the-blank questions.
    Returns a list of tuples: (question_text, choices, correct_answer)
    """
    ensure_nltk_data()
    blob = TextBlob(text)
    sposs = {}

    for sentence in blob.sentences:
        sent_str = str(sentence)
        poss = {}
        for word, tag in sentence.tags:
            if tag not in poss:
                poss[tag] = []
            poss[tag].append(word)
        sposs[sent_str] = poss

    questions_data = []

    for sent_str, poss in sposs.items():
        words_list1, osentence, replaced = remove_word(sent_str, poss)
        if replaced is None:
            continue

        target_words = poss.get('NNP') or poss.get('NN') or []
        distinct_candidates = list(dict.fromkeys(target_words))

        for w in blob.words:
            if len(distinct_candidates) >= 4:
                break
            if w not in distinct_candidates and len(w) > 2:
                distinct_candidates.append(str(w))

        correct_answer = words_list1[0]
        options = [correct_answer]
        distractors = [num for num in distinct_candidates if num.lower() != correct_answer.lower()]
        options.extend(distractors[:3])

        # Fill remaining options if fewer than 4 distractors were found
        while len(options) < 4:
            dummy = f"Option_{len(options) + 1}"
            if dummy not in options:
                options.append(dummy)

        random.shuffle(options)
        questions_data.append((replaced, options, correct_answer))

    return questions_data


def main():
    filename = sys.argv[1] if len(sys.argv) > 1 else 'in.txt'

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = f.read()
    except Exception as e:
        print(f"Error reading file '{filename}': {e}")
        sys.exit(1)

    questions = generate_blanks_questions(data)

    print(f"\nGenerated {len(questions)} Fill-in-the-Blank Questions:\n")
    for idx, (q_text, choices, answer) in enumerate(questions, 1):
        print(f"{idx}: {q_text}")
        print("Possible answers are:")
        for c_idx, choice in enumerate(choices, 1):
            print(f"  {c_idx}: {choice}")
        print(f"Correct Answer: {answer}")
        print("\n" + "=" * 40 + "\n")


if __name__ == "__main__":
    main()
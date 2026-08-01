"""
Fill-in-the-Blanks Question Generator with Smart Distractor Generation.
Uses NLP POS tagging and WordNet semantic lookup to create realistic multiple-choice options.
"""

import sys
import random
import re
import nltk
from nltk.corpus import wordnet
from textblob import TextBlob


def ensure_nltk_data():
    """Ensure required NLTK data packages are downloaded."""
    packages = [
        'punkt',
        'punkt_tab',
        'averaged_perceptron_tagger',
        'averaged_perceptron_tagger_eng',
        'wordnet',
        'brown',
    ]
    for pkg in packages:
        try:
            nltk.download(pkg, quiet=True)
        except Exception:
            pass


def get_wordnet_distractors(target_word, pos_tag='n', max_count=3):
    """Fetch smart distractors using WordNet synsets/hypernyms/hyponyms."""
    distractors = set()
    synsets = wordnet.synsets(target_word, pos=pos_tag)
    if not synsets:
        synsets = wordnet.synsets(target_word)

    for syn in synsets:
        # Get hyponyms (more specific words)
        for hyper in syn.hypernyms():
            for hypo in hyper.hyponyms():
                for lemma in hypo.lemmas():
                    name = lemma.name().replace('_', ' ')
                    if name.lower() != target_word.lower() and len(name) > 2:
                        distractors.add(name.capitalize() if target_word[0].isupper() else name)
                    if len(distractors) >= max_count:
                        break
                if len(distractors) >= max_count:
                    break

        if len(distractors) >= max_count:
            break

    return list(distractors)[:max_count]


def replace_case_insensitive(word, sentence_text):
    """Replace word with blank line case-insensitively."""
    pattern = re.compile(r'\b' + re.escape(word) + r'\b', re.IGNORECASE)
    result, count = pattern.subn('__________________', sentence_text)
    if count == 0:
        result = sentence_text.replace(word, '__________________')
    return result


def remove_word(sentence_text, pos_dict):
    """Select target noun (prioritize Proper Noun NNP over NN)."""
    words = None
    if 'NNP' in pos_dict and pos_dict['NNP']:
        words = pos_dict['NNP']
    elif 'NN' in pos_dict and pos_dict['NN']:
        words = pos_dict['NN']
    else:
        return (None, sentence_text, None)

    if words:
        target_word = words[0]
        replaced_text = replace_case_insensitive(target_word, sentence_text)
        return (target_word, sentence_text, replaced_text)

    return (None, sentence_text, None)


def generate_blanks_questions(text):
    """
    Parses sentences and generates fill-in-the-blank questions with smart distractors.
    Returns list of tuples: (question_text, choices_list, correct_answer)
    """
    ensure_nltk_data()
    blob = TextBlob(text)
    sposs = {}

    for sentence in blob.sentences:
        sent_str = str(sentence).strip()
        if not sent_str:
            continue
        poss = {}
        for word, tag in sentence.tags:
            if tag not in poss:
                poss[tag] = []
            poss[tag].append(word)
        sposs[sent_str] = poss

    questions_data = []

    for sent_str, poss in sposs.items():
        target_word, osentence, replaced = remove_word(sent_str, poss)
        if not target_word or replaced == sent_str:
            continue

        # 1. Try WordNet smart distractors
        distractors = get_wordnet_distractors(target_word, pos_tag='n', max_count=3)

        # 2. Fallback to same-POS words from document text
        same_pos_candidates = poss.get('NNP') or poss.get('NN') or []
        for w in same_pos_candidates + [str(bw) for bw in blob.words]:
            if len(distractors) >= 3:
                break
            w_str = str(w).strip()
            if (w_str.lower() != target_word.lower() and 
                w_str not in distractors and 
                len(w_str) > 2 and 
                w_str.isalpha()):
                distractors.append(w_str.capitalize() if target_word[0].isupper() else w_str)

        # Build 4 choices
        options = [target_word] + distractors[:3]
        
        # Ensure 4 unique choices
        while len(options) < 4:
            dummy = f"Choice_{len(options) + 1}"
            if dummy not in options:
                options.append(dummy)

        random.shuffle(options)
        questions_data.append((replaced, options, target_word))

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
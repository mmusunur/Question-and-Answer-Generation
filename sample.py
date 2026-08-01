"""
Probability-based Question Answering Classifier.
"""

import sys
from tabulate import tabulate

TAGS = ["expl", "adj", "noun", "nsubj", "verb", "prep", "det", "pobj", "punct", "conj", "pron", "dobj", "adv", "tmod"]

WHWORDSPROB = [
    ("what", [("noun", 30), ("nsubj", 30), ("adj", 40), ("dobj", 40)]),
    ("where", [("prep", 50), ("pobj", 50)]),
    ("how", [("adj", 50), ("amod", 50)]),
    ("how many", [("num", 70), ("adj", 30)]),
    ("whose", [("noun", 40), ("pron", 40), ("nsubj", 40)]),
    ("whom", [("noun", 40), ("pron", 60), ("nsubj", 60)]),
    ("who", [("noun", 40), ("pron", 40), ("nsubj", 40)]),
    ("when", [("tmod", 80)])
]

WHWORDS = [
    ("what", ["noun", "nsubj", "adj", "amod", "dobj"]),
    ("where", ["prep", "pobj"]),
    ("how", ["adj", "amod", "adv"]),
    ("how many", ["num", "adj"]),
    ("whose", ["noun", "pron", "nsubj"]),
    ("which", ["adj", "amod"]),
    ("whom", ["noun", "pron", "nsubj"]),
    ("who", ["noun", "pron", "nsubj"]),
    ("when", ["tmod"])
]


def remove_question_words(sentence_data, question_words):
    """Remove question words from sentence tuples."""
    result = []
    for tup in sentence_data:
        if tup[0] not in question_words:
            result.append(tup)
    return result


def get_wh_word_tags(whword):
    for tup in WHWORDS:
        if tup[0] == whword:
            return tup[1]
    return []


def get_prob_table(whword):
    for tup in WHWORDSPROB:
        if tup[0] == whword:
            return tup[1]
    return []


def get_prob(prob_table, word):
    for tup in prob_table:
        if tup[0] == word:
            return tup[1]
    return 0


def ask_question(sentence_data, whword):
    whwordtyp = get_wh_word_tags(whword)
    probtable = get_prob_table(whword)
    ans = []
    for tup in sentence_data:
        count = 0
        prob = 0
        for typ in tup[1]:
            if typ in whwordtyp:
                count += 1
                prob += get_prob(probtable, typ)
        if count > 0:
            ans.append((tup[0], count, prob))
    return ans


def main():
    filename = sys.argv[1] if len(sys.argv) > 1 else "file1.txt"
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error opening file '{filename}': {e}")
        return

    parsed_lines = []
    for ll in lines:
        parts = ll.lower().strip().split("\t")
        if len(parts) > 2:
            parsed_lines.append((parts[1], parts[2:]))

    sentence_data = []
    for word, tags in parsed_lines:
        valid_tags = [t for t in tags if t in TAGS]
        sentence_data.append((word, valid_tags))

    print("\n--- POS Tags ---")
    print(TAGS)
    print("\n--- Parsed Sentence Tokens ---")
    print(sentence_data)

    if not sentence_data:
        print("No tab-separated tag data found in input file.")
        return

    question_str = input("\nEnter question: ").strip().lower()
    question_words = question_str.split()

    if not question_words:
        print("No question entered.")
        return

    filtered_sentence = remove_question_words(sentence_data, question_words)
    ans = ask_question(filtered_sentence, question_words[0])

    print("\nCandidate Answers:")
    if ans:
        headers = ["Candidate Word", "Match Count", "Probability Score"]
        print(tabulate(ans, headers=headers, tablefmt="grid"))
    else:
        print("No matching answers found.")


if __name__ == "__main__":
    main()

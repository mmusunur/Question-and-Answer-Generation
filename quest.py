"""
Advanced Question Generation Engine.
Generates What, Who, Where, When, and How Many questions using NLP syntactic parsing and named entity recognition.
"""

import sys
import re
import nltk
from textblob import TextBlob, Word


def ensure_nltk_data():
    """Ensure required NLTK data packages are downloaded."""
    packages = [
        'punkt',
        'punkt_tab',
        'averaged_perceptron_tagger',
        'averaged_perceptron_tagger_eng',
        'maxent_ne_chunker',
        'maxent_ne_chunker_tab',
        'words',
        'wordnet',
    ]
    for pkg in packages:
        try:
            nltk.download(pkg, quiet=True)
        except Exception:
            pass


def extract_named_entities(sentence_str):
    """Extract Named Entities using NLTK chunking."""
    tokens = nltk.word_tokenize(sentence_str)
    tagged = nltk.pos_tag(tokens)
    tree = nltk.chunk.ne_chunk(tagged)
    entities = []
    for node in tree:
        if isinstance(node, nltk.Tree):
            entity_name = " ".join([token for token, tag in node.leaves()])
            entity_type = node.label()
            entities.append((entity_name, entity_type))
    return entities


def gen_ne_questions(sentence_str):
    """Generate Who, Where, When, and How Many questions based on Named Entities."""
    questions = []
    entities = extract_named_entities(sentence_str)
    tokens = nltk.word_tokenize(sentence_str)
    tagged = nltk.pos_tag(tokens)

    for entity_name, entity_type in entities:
        if entity_type == 'PERSON':
            # Replace Person with Who
            q = re.sub(re.escape(entity_name), "Who", sentence_str, count=1, flags=re.IGNORECASE)
            q = q.rstrip(".!?") + "?"
            questions.append((q, entity_name, "Who"))

        elif entity_type in ['GPE', 'LOCATION']:
            # Check for preposition before location (e.g., in Minsk, at Paris)
            prep_pattern = r'\b(in|at|from|to|near)\s+' + re.escape(entity_name)
            if re.search(prep_pattern, sentence_str, re.IGNORECASE):
                q = re.sub(prep_pattern, "where", sentence_str, count=1, flags=re.IGNORECASE)
            else:
                q = re.sub(re.escape(entity_name), "where", sentence_str, count=1, flags=re.IGNORECASE)
            q = q.strip()
            if q:
                q = q[0].upper() + q[1:]
                q = q.rstrip(".!?") + "?"
                questions.append((q, entity_name, "Where"))

        elif entity_type in ['DATE', 'TIME']:
            prep_pattern = r'\b(in|at|on|during|around)\s+' + re.escape(entity_name)
            if re.search(prep_pattern, sentence_str, re.IGNORECASE):
                q = re.sub(prep_pattern, "when", sentence_str, count=1, flags=re.IGNORECASE)
            else:
                q = re.sub(re.escape(entity_name), "when", sentence_str, count=1, flags=re.IGNORECASE)
            q = q.strip()
            if q:
                q = q[0].upper() + q[1:]
                q = q.rstrip(".!?") + "?"
                questions.append((q, entity_name, "When"))

    return questions


def genQuestion(line):
    """
    Generates a question from a given sentence (TextBlob or string object).
    Returns the generated question string or empty string if no rule matches.
    """
    sentence_str = str(line).strip()
    if not sentence_str:
        return ''

    if isinstance(line, str):
        line = TextBlob(line)

    bucket = {}
    for i, (word, tag) in enumerate(line.tags):
        if tag not in bucket:
            bucket[tag] = i

    question = ''

    # First check Named Entity questions for Who/Where/When
    ne_qs = gen_ne_questions(sentence_str)
    if ne_qs:
        return ne_qs[0][0]

    # Rule tag combinations for What questions
    l1 = ['NNP', 'VBG', 'VBZ', 'IN']
    l2 = ['NNP', 'VBG', 'VBZ']
    l3 = ['PRP', 'VBG', 'VBZ', 'IN']
    l4 = ['PRP', 'VBG', 'VBZ']
    l7 = ['NN', 'VBG', 'VBZ']
    l8 = ['NNP', 'VBZ', 'JJ']
    l9 = ['NNP', 'VBZ', 'NN']
    l10 = ['NNP', 'VBZ']
    l11 = ['PRP', 'VBZ']
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
        if q and q not in questions:
            questions.append(q)

    return questions


def main():
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

    questions = parse(textinput)
    for q in questions:
        print('Question: ', q)


if __name__ == "__main__":
    main()

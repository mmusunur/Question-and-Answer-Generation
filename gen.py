"""
Named Entity Tree Traversal Demo using NLTK.
"""

import nltk


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
    ]
    for pkg in packages:
        try:
            nltk.download(pkg, quiet=True)
        except Exception:
            pass


ROOT = 'ROOT'


def getNodes(parent):
    """Traverse tree nodes and display named entities and POS tokens."""
    for node in parent:
        if isinstance(node, nltk.Tree):
            if node.label() == ROOT:
                print("======== Sentence =========")
                print("Sentence:", " ".join(node.leaves()))
            else:
                print("Label:", node.label())
                print("Leaves:", node.leaves())

            getNodes(node)
        else:
            print("Word:", node)


def main():
    ensure_nltk_data()
    sentence = "Sam plays cricket at 5AM in New York."
    tokens = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokens)
    entities = nltk.chunk.ne_chunk(tagged)

    print("Parsed Named Entities:")
    getNodes(entities)


if __name__ == "__main__":
    main()
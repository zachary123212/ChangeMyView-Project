import operator
import os
import pickle
import pprint

import nltk
from nltk import RegexpTokenizer

from src.Reader import read

# Global Variables:

pp = pprint.PrettyPrinter(indent=4, width=100, depth=6)
lemmatizer = nltk.WordNetLemmatizer()
tokenizer = RegexpTokenizer(r'\w+')

CONCESSIONS = ["nevertheless", "nonetheless", "non the less", "however", "admittedly", "but", "although", "though",
               "even though", "even if", "even when", "even so", "whereas", "while", "in spite of", "despite",
               "notwithstanding", "albeit", "on the one hand", "on the other hand", "acknowledge", "concede", "admit",
               "admitting that", "grant", "granting that", "the fact remains that"]


# Main Procedure:

def main():
    with open("data/data.pickle", 'r+b') as raw:
        if os.stat("data/data.pickle").st_size == 0:
            pickle.dump(read("data/train_pair_data.jsonlist"), raw)
            print("data serialized")
        data_p = pickle.load(raw)
        print("data loaded")

    texts_p = [[comment['text_plain'] for comment in thread['positive']] for thread in data_p]
    texts_p = [t[0] for t in texts_p if t != []]

    texts_n = [[comment['text_plain'] for comment in thread['negative']] for thread in data_p]
    texts_n = [t[0] for t in texts_n if t != []]

    concession_frequencies_p = {}
    word_count_p = 0

    concession_frequencies_n = {}
    word_count_n = 0

    for text in texts_p:
        word_count_p += len(tokenizer.tokenize(text))
    for text in texts_n:
        word_count_n += len(tokenizer.tokenize(text))

    for concession in CONCESSIONS:
        concession_frequencies_p[concession] = []
        concession_frequencies_n[concession] = []

        concession_frequencies_p[concession].append(0)
        concession_frequencies_n[concession].append(0)

        for text in texts_p:
            if concession in text:
                concession_frequencies_p[concession][0] += 1

                # concession_frequencies_p[concession][0] += text.count(concession)
        for text in texts_n:
            if concession in text:
                concession_frequencies_n[concession][0] += 1

                # concession_frequencies_n[concession][0] += text.count(concession)

        concession_frequencies_p[concession].append(concession_frequencies_p[concession][0] / len(texts_p))
        concession_frequencies_n[concession].append(concession_frequencies_n[concession][0] / len(texts_n))

        # concession_frequencies_p[concession].append(concession_frequencies_p[concession][0] / word_count_p)
        # concession_frequencies_n[concession].append(concession_frequencies_n[concession][0] / word_count_n)

    with open("data/results.txt", "w") as raw:
        print("positive:\n")
        pp.pprint(sorted(concession_frequencies_p.items(), key=operator.itemgetter(1), reverse=True))

        raw.write("positive:\n")
        raw.write(pp.pformat(sorted(concession_frequencies_p.items(), key=operator.itemgetter(1), reverse=True)))

        print("\n\nnegative:\n")
        pp.pprint(sorted(concession_frequencies_n.items(), key=operator.itemgetter(1), reverse=True))

        raw.write("\n\nnegative:\n")
        raw.write(pp.pformat(sorted(concession_frequencies_n.items(), key=operator.itemgetter(1), reverse=True)))


if __name__ == "__main__":
    main()

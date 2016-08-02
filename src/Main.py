import csv
import operator
import os
import pickle
import pprint
import re

import nltk
from nltk import RegexpTokenizer

from src import Csv
from src import Plot
from src import XMLWriter
from src.Reader import read

# Global Variables:

pp = pprint.PrettyPrinter(indent=4, width=200, depth=6)
lemmatizer = nltk.WordNetLemmatizer()
tokenizer = RegexpTokenizer(r'\w+')

field_names = ['thread_id', 'comment_id', 'context']

CONCESSIONS = ["nevertheless", "nonetheless", "non the less", "however", "but", "although", "though",
               "even though", "even if", "even when", "even so", "whereas", "while", "in spite of", "despite",
               "notwithstanding", "albeit", "on the one hand", "on the other hand",
               "the fact remains that"]

CONCESSIONS_RE = [re.compile("\\b" + concession + "\\b") for concession in CONCESSIONS]

CONCESSIONS.append("admit")
CONCESSIONS_RE.append(re.compile('\\b(?:I|I\'ll)(?:\\b\\S*\\s){0,5}admit\\b'))

CONCESSIONS.append("concede")
CONCESSIONS_RE.append(re.compile('\\b(?:I|I\'ll)(?:\\b\\S*\\s){0,5}concede\\b'))

# Serialized Data Reading/Writing

with open("data/data.pickle", 'r+b') as raw:
    if os.stat("data/data.pickle").st_size == 0:
        pickle.dump(read("data/train_pair_data.jsonlist"), raw)
        print("data serialized")
    data_p = pickle.load(raw)
    print("data loaded")


def write_to_csv(concession, concession_re, register):
    with open("data/output/" + concession.replace(" ", "_") + "_" + register + ".csv", "w+", encoding="utf-8") as raw:
        writer = csv.DictWriter(raw, fieldnames=field_names)
        writer.writeheader()

        for post in data_p:
            for comment in post[register]:
                for sentence_i in range(0, len(comment['text_sentences'])):
                    if re.search(concession_re, comment['text_sentences'][sentence_i]):
                        displayed_sentences = ""
                        if concession == "but":
                            if comment['text_tokenized'][sentence_i][0].lower() == "but":
                                try:
                                    displayed_sentences += comment['text_sentences'][sentence_i - 1] + " "
                                except:
                                    pass

                                try:
                                    displayed_sentences += comment['text_sentences'][sentence_i]
                                except:
                                    pass
                            else:
                                try:
                                    displayed_sentences += comment['text_sentences'][sentence_i]
                                except:
                                    pass

                        # TODO: refactor this

                        elif concession == "however":
                            if comment['text_tokenized'][sentence_i][0].lower() == "however":
                                try:
                                    displayed_sentences += comment['text_sentences'][sentence_i - 1] + " "
                                except:
                                    pass

                                try:
                                    displayed_sentences += comment['text_sentences'][sentence_i]
                                except:
                                    pass
                            else:
                                try:
                                    displayed_sentences += comment['text_sentences'][sentence_i]
                                except:
                                    pass

                        elif concession == "while" or concession == "whereas":
                            try:
                                displayed_sentences += comment['text_sentences'][sentence_i]
                            except:
                                pass

                        else:
                            try:
                                displayed_sentences += comment['text_sentences'][sentence_i - 1] + " "
                            except:
                                pass
                            displayed_sentences += comment['text_sentences'][sentence_i] + " "
                            try:
                                displayed_sentences += comment['text_sentences'][sentence_i + 1]
                            except:
                                pass

                        writer.writerow(
                            {'thread_id': post['op_name'], 'comment_id': comment['id'],
                             'context': displayed_sentences})


# Main Procedure:
def main():

    # print(len(data_p))
    # return

    # Write to XML

    XMLWriter.dump(data_p)

    return
    # Text Extraction

    texts_p = [[comment['text_plain'] for comment in thread['positive']] for thread in data_p]
    texts_p = [t[0] for t in texts_p if t != []]

    texts_n = [[comment['text_plain'] for comment in thread['negative']] for thread in data_p]
    texts_n = [t[0] for t in texts_n if t != []]

    # Concession Calculation

    concession_frequencies_p = {}
    concession_frequencies_n = {}

    for concession_i in range(0, len(CONCESSIONS)):
        concession_frequencies_p[CONCESSIONS[concession_i]] = []
        concession_frequencies_n[CONCESSIONS[concession_i]] = []

        concession_frequencies_p[CONCESSIONS[concession_i]].append(0)
        concession_frequencies_n[CONCESSIONS[concession_i]].append(0)

        for post in texts_p:
            if re.search(CONCESSIONS_RE[concession_i], post):
                concession_frequencies_p[CONCESSIONS[concession_i]][0] += 1
        for post in texts_n:
            if re.search(CONCESSIONS_RE[concession_i], post):
                concession_frequencies_n[CONCESSIONS[concession_i]][0] += 1

        concession_frequencies_p[CONCESSIONS[concession_i]].append(
            concession_frequencies_p[CONCESSIONS[concession_i]][0] / len(texts_p))
        concession_frequencies_n[CONCESSIONS[concession_i]].append(
            concession_frequencies_n[CONCESSIONS[concession_i]][0] / len(texts_n))

    # Write to CSV

    for concession_i in range(0, len(CONCESSIONS)):
        write_to_csv(CONCESSIONS[concession_i], CONCESSIONS_RE[concession_i], "positive")
        write_to_csv(CONCESSIONS[concession_i], CONCESSIONS_RE[concession_i], "negative")

        Csv.write_word_comment_position(data_p, CONCESSIONS[concession_i], CONCESSIONS_RE[concession_i], "positive")
        Csv.write_word_comment_position(data_p, CONCESSIONS[concession_i], CONCESSIONS_RE[concession_i], "negative")

    # Chart Compilation

    for concession in CONCESSIONS:
        Plot.calc(data_p, concession, "positive")
        Plot.calc(data_p, concession, "negative")

    # Print Output

    with open("data/results.txt", "w") as raw:
        # print("positive:\n")
        # pp.pprint(sorted(concession_frequencies_p.items(), key=operator.itemgetter(1), reverse=True))

        raw.write("positive:\n")
        raw.write(pp.pformat(sorted(concession_frequencies_p.items(), key=operator.itemgetter(1), reverse=True)))

        # print("\n\nnegative:\n")
        # pp.pprint(sorted(concession_frequencies_n.items(), key=operator.itemgetter(1), reverse=True))

        raw.write("\n\nnegative:\n")
        raw.write(pp.pformat(sorted(concession_frequencies_n.items(), key=operator.itemgetter(1), reverse=True)))


if __name__ == "__main__":
    main()

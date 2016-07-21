import csv
import operator
import os
import pickle
import pprint
import re

import nltk
from nltk import RegexpTokenizer

from src.Reader import read

# Global Variables:

pp = pprint.PrettyPrinter(indent=4, width=200, depth=6)
lemmatizer = nltk.WordNetLemmatizer()
tokenizer = RegexpTokenizer(r'\w+')

CONCESSIONS = ["nevertheless", "nonetheless", "non the less", "however", "but", "although", "though",
               "even though", "even if", "even when", "even so", "whereas", "while", "in spite of", "despite",
               "notwithstanding", "albeit", "on the one hand", "on the other hand",
               "the fact remains that"]

CONCESSIONS_RE = [re.compile("\\b" + concession + "\\b") for concession in CONCESSIONS]

CONCESSIONS.append("admit")
CONCESSIONS_RE.append(re.compile('\\b(?:I|I\'ll)(?:\\b\\S*\\s){0,5}admit\\b'))

CONCESSIONS.append("concede")
CONCESSIONS_RE.append(re.compile('\\b(?:I|I\'ll)(?:\\b\\S*\\s){0,5}concede\\b'))


# Main Procedure:
def main():
    # data = []
    #
    # with open("data/train_pair_data.jsonlist", "r") as raw:
    #     for line in raw.readlines():
    #         data.append(json.loads(line))
    #
    # print(data[0]['op_name'])
    # print(data[0]['positive']['comments'][0].keys())
    # return

    # Serialized Data Reading/Writing

    with open("data/data.pickle", 'r+b') as raw:
        if os.stat("data/data.pickle").st_size == 0:
            pickle.dump(read("data/train_pair_data.jsonlist"), raw)
            print("data serialized")
        data_p = pickle.load(raw)
        print("data loaded")

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

    field_names = ['thread_id', 'comment_id', 'context']

    for concession_i in range(0, len(CONCESSIONS)):
        with open("data/output/" + CONCESSIONS[concession_i].replace(" ", "_") + "_positive.csv", "w+",
                  encoding="utf-8") as raw:
            writer = csv.DictWriter(raw, fieldnames=field_names)
            writer.writeheader()

            for post in data_p:
                for comment in post['positive']:
                    for sentence_i in range(0, len(comment['text_sentences'])):
                        if re.search(CONCESSIONS_RE[concession_i], comment['text_sentences'][sentence_i]):
                            displayed_sentences = ""
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

        with open("data/output/" + CONCESSIONS[concession_i].replace(" ", "_") + "_negative.csv", "w+",
                  encoding="utf-8") as raw:
            writer = csv.DictWriter(raw, fieldnames=field_names)
            writer.writeheader()

            for post in data_p:
                for comment in post['negative']:
                    for sentence_i in range(0, len(comment['text_sentences'])):
                        if re.search(CONCESSIONS_RE[concession_i], comment['text_sentences'][sentence_i]):
                            displayed_sentences = ""
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
    # Print Output

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

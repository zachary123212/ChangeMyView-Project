import csv

from nltk import word_tokenize, re

fieldnames = ['sentence_position', "sentence_count"]


def write_word_comment_position(data_p, input_word, input_re, register):
    with open("data/positions/" + input_word.replace(" ", "_") + "_" + register + ".csv", "w+") as raw:
        writer = csv.DictWriter(raw, fieldnames=fieldnames)
        writer.writeheader()

        for thread in data_p:
            for comment in thread[register]:
                for sentence_i in range(0, len(comment['text_sentences'])):
                    if re.search(input_re, comment['text_sentences'][sentence_i]):
                        writer.writerow({'sentence_position': sentence_i + 1, 'sentence_count': sentence_i})

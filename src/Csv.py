import csv

from nltk import word_tokenize

fieldnames = ['sentence_position', "sentence_count"]


def write_word_comment_position(data_p, input_word, register):
    word_length = len(word_tokenize(input_word))

    with open("data/positions/" + input_word.replace(" ", "_") + "_" + register + ".csv", "w+") as raw:
        writer = csv.DictWriter(raw, fieldnames=fieldnames)
        writer.writeheader()

        for thread in data_p:
            for comment in thread[register]:
                for sentence_i in range(0, len(comment['text_tokenized'])):
                    sentence_count = len(comment['text_tokenized'])
                    for word_i in range(0, len(comment['text_tokenized'][sentence_i])):
                        if input_word == " ".join(
                                [word for word in
                                 comment['text_tokenized'][sentence_i][word_i:(word_i + word_length)]]):
                            writer.writerow({'sentence_position': sentence_i + 1, 'sentence_count': sentence_count})

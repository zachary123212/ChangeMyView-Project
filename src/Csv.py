import csv

from nltk import word_tokenize, re, sent_tokenize

fieldnames = ['sentence_position', "sentence_count", "paragraph_position", "paragraph_count"]


def write_word_comment_position(data_p, input_word, input_re, register):
    with open("data/positions/" + input_word.replace(" ", "_") + "_" + register + ".csv", "w+") as raw:
        writer = csv.DictWriter(raw, fieldnames=fieldnames)
        writer.writeheader()

        for thread in data_p:
            for comment in thread[register]:
                last_sentence = 1
                sentence_count = len(comment['text_sentences'])
                for paragraph_i in range(0, len(comment['text_paragraphs'])):
                    sentence_tokenized = sent_tokenize(comment['text_paragraphs'][paragraph_i])
                    for sentence_i in range(0, len(sentence_tokenized)):
                        if re.search(input_re, sentence_tokenized[sentence_i]):
                            writer.writerow(
                                {'sentence_position': last_sentence + sentence_i,
                                 'sentence_count': sentence_count,
                                 'paragraph_position': paragraph_i + 1, 'paragraph_count': len(sentence_tokenized)})
                    last_sentence += len(sentence_tokenized)

                    # for sentence_i in range(0, len(comment['text_sentences'])):
                    #     if re.search(input_re, comment['text_sentences'][sentence_i]):
                    #         writer.writerow({'sentence_position': sentence_i + 1, 'sentence_count': sentence_i})

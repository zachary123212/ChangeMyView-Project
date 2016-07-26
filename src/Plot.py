import matplotlib.pyplot as plt
from nltk import word_tokenize


def calc(data_p, input_word, register):
    freqs = []
    word_length = len(word_tokenize(input_word))

    fig = plt.figure()
    ax = fig.add_subplot(111)

    for thread in data_p:
        for comment in thread[register]:
            for sentence_i in range(0, len(comment['text_tokenized'])):
                for word_i in range(0, len(comment['text_tokenized'][sentence_i])):
                    if input_word == " ".join(
                            [word for word in comment['text_tokenized'][sentence_i][word_i:(word_i + word_length)]]):
                        freqs.append((sentence_i + 1)/len(comment['text_tokenized']))

    ax.hist(freqs, 5, color='green', alpha=0.8)
    plt.savefig("data/hist/" + input_word.replace(" ", "_") + "_" + register + ".png")
    plt.close()

import matplotlib.pyplot as plt


def calc(data_p, input_word, register):
    freqs = []

    fig = plt.figure()
    ax = fig.add_subplot(111)

    for thread in data_p:
        for comment in thread[register]:
            for sentence_i in range(0, len(comment['text_tokenized'])):
                for word in comment['text_tokenized'][sentence_i]:
                    if word.lower() == input_word:
                        freqs.append(sentence_i / len(comment['text_tokenized']))
    ax.hist(freqs, 20, color='green', alpha=0.8)
    plt.savefig("data/hist/" + input_word.replace(" ", "_") + "_" + register + ".png")
    plt.close()

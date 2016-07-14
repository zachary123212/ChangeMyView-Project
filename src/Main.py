import operator
import os
import pickle
import pprint

import nltk

from src.Reader import read

# Global Variables:

pp = pprint.PrettyPrinter(indent=4, width=100, depth=6)
lemmatizer = nltk.WordNetLemmatizer()
tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')

CONCESSIONS = ["although", "albeit", "fog all", "all the same", "however", "anyway", "even though", "even so",
               "despite", "in spite of", "nevertheless", "nonetheless", "notwithstanding", "just the same",
               "regardless", "still", "yet"]


# Main Procedure:

def main():
    with open("data/data.pickle", 'r+b') as raw:
        if os.stat("data/data.pickle").st_size == 0:
            pickle.dump(read("/data/train_pair_data.jsonlist"), raw)
            print("data serialized")
        data_p = pickle.load(raw)
        print("data loaded")

    texts_p = [[comment['text_plain'] for comment in thread['positive']] for thread in data_p]
    texts_p = [t[0] for t in texts_p if t != []]

    texts_n = [[comment['text_plain'] for comment in thread['negative']] for thread in data_p]
    texts_n = [t[0] for t in texts_n if t != []]

    # trigrams = []

    # for text in texts:
    #     text = re.sub(r'((http|https)://)?(www(0-9)?.)?\w*\.((\w\w\w)|(\w\w)|(\w\w\.\w\w))', 'URL', text,
    #                   flags=re.MULTILINE)

    # tokens = tokenizer.tokenize(text)
    #
    # tokens = [token.lower() for token in tokens if len(token) > 1]
    #
    # tokens = [word for word in tokens if word not in nltk.corpus.stopwords.words('english')]
    #
    # trigrams += nltk.trigrams(tokens)

    # freqs = nltk.FreqDist(trigrams)
    # pp.pprint(freqs.most_common(50))

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
            concession_frequencies_p[concession][0] += text.count(concession)
        for text in texts_n:
            concession_frequencies_n[concession][0] += text.count(concession)

        concession_frequencies_p[concession].append(concession_frequencies_p[concession][0] / word_count_p)
        concession_frequencies_n[concession].append(concession_frequencies_n[concession][0] / word_count_n)

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

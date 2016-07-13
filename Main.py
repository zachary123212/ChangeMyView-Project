import os
import pickle
import pprint
import nltk

from Reader import read

# Global Variables:

pp = pprint.PrettyPrinter(indent=4, width=100, depth=6)
lemmatizer = nltk.WordNetLemmatizer()
tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')


# Main Procedure:

def main():
    with open("data.pickle", 'r+b') as raw:
        if os.stat("data.pickle").st_size == 0:
            pickle.dump(read("train_pair_data.jsonlist"), raw)
        data_p = pickle.load(raw)

    texts = [[comment['text_plain'] for comment in thread['positive']] for thread in data_p]
    texts = [t[0] for t in texts if t != []]

    trigrams = []

    for text in texts:
        tokens = tokenizer.tokenize(text)
        tokens = [token.lower() for token in tokens if len(token) > 1]

        tokens = [word for word in tokens if word not in nltk.corpus.stopwords.words('english')]

        trigrams += nltk.trigrams(tokens)

    freqs = nltk.FreqDist(trigrams)
    pp.pprint(freqs.most_common(50))

if __name__ == "__main__":
    main()

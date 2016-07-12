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

    texts = [thread['op_text_plain'] for thread in data_p]
    bigrams = []

    for text in texts[:50]:
        tokens = tokenizer.tokenize(text)
        tokens = [token.lower() for token in tokens if len(token) > 1]

        # tokens_l = []
        tokens = [word for word in tokens if word not in nltk.corpus.stopwords.words('english')]

        # for token in tokens:
        #     tokens_l.append(lemmatizer.lemmatize(token))

        # tokens = tokens_l

        bigrams += nltk.bigrams(tokens)

    freqs = nltk.FreqDist(bigrams)

    pp.pprint(freqs.most_common(50))

if __name__ == "__main__":
    main()

import os
import pickle
import pprint

from Reader import read

pp = pprint.PrettyPrinter(indent=4, width=100, depth=6)

with open("data.pickle", 'r+b') as raw:
    if os.stat("data.pickle").st_size == 0:
        pickle.dump(read("train_pair_data.jsonlist"), raw)
    data_p = pickle.load(raw)

# for thread in data_p:
#     for comment in [thread['op_text']] + [comment['text'] for comment in thread['positive'] + thread['negative']]:
#         pp.pprint(comment)


comment = data_p[1]['positive'][0]['text_plain']
print(comment)

# for paragraph in [[text[1] for text in chunk[1]] for chunk in data_p[2]['op_text']]:
#     text = paragraph[0]
#     words = word_tokenize(text)
#
#     print(nltk.FreqDist(words).tabulate())
#
#     # print(words.count("the"))

import pprint
import os
import pickle
from Reader import read

pp = pprint.PrettyPrinter(indent=4, width=100, depth=6)

with open("data.pickle", 'rb') as raw:
    if os.stat("data.pickle").st_size == 0:
        pickle.dump(read("train_pair_data.jsonlist"), raw)
    data_p = pickle.load(raw)

for thread in data_p:
    for comment in [thread['op_text']] + [comment['text'] for comment in thread['positive'] + thread['negative']]:
        pp.pprint(comment)


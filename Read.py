import json
import pprint
from pyparsing import ParserElement

# for some weird reason, the code only seems to work when you run it twice. WHY?
exec(open("Parser.py").read())
exec(open("Parser.py").read())

data = []

with open("train_pair_data.jsonlist", "r") as raw:
    for line in raw.readlines():
        data.append(json.loads(line))

def process_text(input_text):
    return input_text.replace("&gt;", ">")

def parse(input_text):
    return markdown.parseString(process_text(input_text)).asList()

# data_p = []
#
# for thread in data:
#     info = {}
#     info['op_author'] = thread['op_author']
#     print(thread['op_text'].encode('utf8'))
#     info['op_text'] = parse(thread['op_text'])
#     info['positive'] = []
#     info['negative'] = []
#
#     for comment in thread['positive']['comments']:
#         infoC = {}
#         infoC['author'] = comment['author']
#         infoC['text'] = parse(comment['body'])
#         info['positive'].append(infoC)
#     for comment in thread['negative']['comments']:
#         infoC = {}
#         infoC['author'] = comment['author']
#         infoC['text'] = parse(comment['body'])
#         info['positive'].append(infoC)
#
# parsed = markdown.parseString(process_text(
#     data[3]['positive']['comments'][1]['body'])).asList()
#
# pp = pprint.PrettyPrinter(indent=4,width=100,depth=6)
#
# pp.pprint(parsed)

test = """
I can't remember **the topic that** spurred this
discussion,
but a friend and I were debating whether man-made things were natural. He took the position that they are unnatural.



He cited this definition by Merriam-Webster:  existing in nature and not made or caused by people : coming from nature (http://www.merriam-webster.com/dictionary/natural) as his basis for the distinction for natural vs. unnatural.

However, I respectfully disagree with his position and furthermore that definition of natural. People arise from nature. Humankind's capacity to create, problem-solve, analyze, rationalize, and build also come from natural processes. How are the things we create unnatural? It is only through natural occurrences that we have this ability, why is it that we would give the credit of these things solely to man, as opposed to nature? We are not separate from nature, thus, how can any of our actions or creations be unnatural? If we were somehow separate from nature, I would understand the distinction between natural and man-made. However, I think unnatural and man-made are not synonyms by any means. It seems to me that man-made things MUST be natural due to our being part of nature.
"""

print(parse(test))

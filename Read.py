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

parsed = markdown.parseString(process_text(
    data[3]['positive']['comments'][1]['body'])).asList()

pp = pprint.PrettyPrinter(indent=4,width=100,depth=6)

pp.pprint(parsed)

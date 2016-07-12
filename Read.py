import json
import pprint
from Parser import markdown

# for some weird reason, the code only seems to work when you run it twice. WHY?
exec(open("Parser.py").read())

# Global Variables:

pp = pprint.PrettyPrinter(indent=4, width=100, depth=6)


# Function Definitions:

def process_text(input_text):
    tmp = input_text
    tmp = tmp.replace("&gt;", ">")
    tmp = tmp.replace("’", "'")
    tmp = tmp.replace("”", "\"")
    return tmp


def parse(input_text):
    return markdown.parseString(process_text(input_text)).asList()


def log(logged_text):
    with open("errors.txt", 'ab') as raw:
        raw.write(b"ERROR:\n")
        raw.write(logged_text.encode('utf-8'))
        raw.write(b"\n")


# Main Procedure:

def main():
    data = []
    data_p = []

    open('errors.txt', 'w').close()

    with open("train_pair_data.jsonlist", "r") as raw:
        for line in raw.readlines():
            data.append(json.loads(line))

    for thread in data:
        info = {}
        info['op_author'] = thread['op_author']
        # print(thread['op_text'])

        try:
            info['op_text'] = parse(thread['op_text'].strip())
        except:
            log(thread['op_text'])
            continue

        # pp.pprint(info['op_text'])
        info['positive'] = []
        info['negative'] = []

        for comment in thread['positive']['comments']:
            info_c = {}
            info_c['author'] = comment['author']
            # print(comment['body'].encode("utf8"))
            try:
                info_c['text'] = parse(comment['body'])
            except:
                log(comment['body'])
                continue
            info['positive'].append(info_c)
        for comment in thread['negative']['comments']:
            info_c = {}
            info_c['author'] = comment['author']
            try:
                info_c['text'] = parse(comment['body'])
            except:
                log(comment['body'])
                continue
            info['negative'].append(info_c)

        data_p.append(info)

    pp.pprint(data_p[:10])

main()

import json

from nltk import RegexpTokenizer, sent_tokenize, pos_tag

from src.Parser import markdown, get_text

# for some weird reason, the code only seems to work when you run it twice. WHY?
exec(open("src/Parser.py").read())

# Global Variables:

tokenizer = RegexpTokenizer(r'\w+')


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
    with open("data/errors.txt", 'ab') as raw:
        raw.write(b"ERROR:\n")
        raw.write(logged_text.encode('utf-8'))
        raw.write(b"\n")


# FileRead Procedure:

def read(file_path):
    data = []
    data_p = []

    open('data/errors.txt', 'w').close()

    with open(file_path, "r") as raw:
        for line in raw.readlines():
            data.append(json.loads(line))

    for thread in data:
        info = {}
        info['op_author'] = thread['op_author']
        info['op_name'] = thread['op_name']

        try:
            info['op_text_structured'] = parse(thread['op_text'].strip())
            info['op_text_plain'] = get_text(info['op_text_structured'])
            info['op_text_sentences'] = sent_tokenize(info['op_text_plain'])
            info['op_text_tokenized'] = [tokenizer.tokenize(sentence) for sentence in info['op_text_sentences']]
        except:
            log(thread['op_text'])
            continue

        info['positive'] = []
        info['negative'] = []

        for comment in thread['positive']['comments']:
            info_c = {}
            info_c['author'] = comment['author']
            info_c['id'] = comment['id']
            try:
                info_c['text_structured'] = parse(comment['body'])
                info_c['text_plain'] = get_text(info_c['text_structured'])
                # info_c['text_paragraphs'] = [" ".join([block[1] for block in paragraph]) for paragraph in
                                             # info_c['text_structured']]
                info_c['text_sentences'] = sent_tokenize(info_c['text_plain'])
                info_c['text_tokenized'] = [tokenizer.tokenize(sentence) for sentence in info_c['text_sentences']]
                info_c['text_tagged'] = [pos_tag(sentence) for sentence in info_c['text_tokenized']]
            except:
                log(comment['body'])
                continue
            info['positive'].append(info_c)
        for comment in thread['negative']['comments']:
            info_c = {}
            info_c['author'] = comment['author']
            info_c['id'] = comment['id']
            try:
                info_c['text_structured'] = parse(comment['body'])
                info_c['text_plain'] = get_text(info_c['text_structured'])
                # info_c['text_paragraphs'] = [" ".join([block[1] for block in paragraph]) for paragraph in
                #                              info_c['text_structured']]
                info_c['text_sentences'] = sent_tokenize(info_c['text_plain'])
                info_c['text_tokenized'] = [tokenizer.tokenize(sentence) for sentence in info_c['text_sentences']]
                info_c['text_tagged'] = [pos_tag(sentence) for sentence in info_c['text_tokenized']]
            except:
                log(comment['body'])
                continue
            info['negative'].append(info_c)

        data_p.append(info)

    return data_p

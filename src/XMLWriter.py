import xml.etree.cElementTree as et


def dump(data_p):
    root = et.Element("cmv-delta-pair")

    for thread_d in data_p:
        thread = et.SubElement(root, "thread")

        op = et.SubElement(thread, "op", author=thread_d['op_author'], id=thread_d['op_name'])
        op.text = thread_d['op_text_plain']

        pos = et.SubElement(thread, "positive")
        for comment_d in thread_d['positive']:
            comment = et.SubElement(pos, "comment", author=comment_d['author'], id=comment_d['id'])

            for paragraph_d in comment_d['text_structured']:
                if paragraph_d[0] == "non-quote":
                    quote = et.SubElement(comment, "non-quote")
                else:
                    quote = et.SubElement(comment, "quote")

                quote.text = " ".join([style[1] for style in paragraph_d[1]])

                # comment.text = comment_d['text_plain']

        neg = et.SubElement(thread, "negative")
        for comment_d in thread_d['negative']:
            comment = et.SubElement(neg, "comment", author=comment_d['author'], id=comment_d['id'])

            for paragraph_d in comment_d['text_structured']:
                if paragraph_d[0] == "non-quote":
                    quote = et.SubElement(comment, "non-quote")
                else:
                    quote = et.SubElement(comment, "quote")

                quote.text = " ".join([style[1] for style in paragraph_d[1]])

                # comment.text = comment_d['text_plain']

    tree = et.ElementTree(root)
    tree.write("data/xml_output.xml")

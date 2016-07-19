from pyparsing import (Suppress, SkipTo, Literal, OneOrMore, Word, ParserElement, StringEnd, printables, Optional,
                       ZeroOrMore, NotAny, alphanums, Combine, oneOf, delimitedList, nums, Group)

# URL Parser (shamelessly stolen from https://www.accelebrate.com/blog/pyparseltongue-parsing-text-with-pyparsing/):

url_chars = alphanums + '-_.~%+'

fragment = Combine((Suppress('#') + Word(url_chars)))('fragment')

scheme = oneOf('http https ftp file')('scheme')
host = Combine(delimitedList(Word(url_chars), '.'))('host')
port = Suppress(':') + Word(nums)('port')
user_info = (
    Word(url_chars)('username') +
    Suppress(':') +
    Word(url_chars)('password') +
    Suppress('@')
)

query_pair = Group(Word(url_chars) + Suppress('=') + Word(url_chars))
query = Group(Suppress('?') + delimitedList(query_pair, '&'))('query')

path = Combine(
    Suppress('/') +
    OneOrMore(~query + Word(url_chars + '/'))
)('path')

url = (
    Optional(
        scheme +
        Suppress('://') +
        user_info
    ) +
    host +
    Optional(port) +
    Optional(path) +
    Optional(query) +
    Optional(fragment)
).setParseAction(lambda t: "URL")

# Back to my own stuff:


# Ex: *this* is italic

italic_text = (
    Suppress(Literal("*")) +
    SkipTo(Literal("*")) +
    Suppress(Literal("*"))
).setParseAction(lambda t: [["italic", t[0]]])

# Ex: **this** is bold

bold_text = (
    Suppress(Literal("**")) +
    SkipTo(Literal("**")) +
    Suppress(Literal("**"))
).setParseAction(lambda t: [["bold", t[0]]])

bold_italic_text = (
    Suppress(Literal("***")) +
    SkipTo(Literal("***")) +
    Suppress(Literal("***"))
).setParseAction(lambda t: [["bold-italic", t[0]]])

link_text = (
    Suppress(Literal("[")) +
    (
        Optional(url) +
        ZeroOrMore(Word(printables.replace("]", ""))).setParseAction(lambda t: "text")
        # SkipTo(Literal("]"))
    ) +
    Suppress(
        Literal("]") +
        Literal("(") +
        SkipTo(Literal(")")) +
        Literal(")")
    )
).setParseAction(lambda t: [["link", t[0]]])

# Ex: this is regular

reg_text = (
    OneOrMore(
        NotAny(
            italic_text |
            link_text
        ) +
        Word(printables) |
        Suppress(Literal("\n")) +
        Word(printables)
    )
    # SkipTo(Literal("*")) | SkipTo(Literal("\n\n"))
).setParseAction(lambda t: [["regular", " ".join(t)]])

# Note: can be either two newlines or the end of the string

line_break = Suppress(
    Literal("\n\n") + ZeroOrMore(Literal("\n")) |
    Literal("\n") + StringEnd() |
    StringEnd()
)

divider = Suppress(OneOrMore(Literal("_")))

text = OneOrMore(link_text | bold_italic_text | bold_text | italic_text | reg_text)

paragraph = (
    OneOrMore(text) +
    line_break
).setParseAction(lambda t: [["non-quote", t.asList()]])

# Ex: > This is a quote

quote = (
    Suppress(Literal(">")) +
    text +
    line_break
).setParseAction(lambda t: [["quote", t.asList()]])

markdown = (
    Suppress(Optional(OneOrMore(Literal("\n")))) +
    OneOrMore(quote | paragraph | divider)
)

ParserElement.setDefaultWhitespaceChars(' \t')


# For Testing purposes:

# test = """
# this is the first paragraph and **it** contains [https://www.google.com and stuff](www.google.com) link
# """
#
# print(markdown.parseString(test))


def flatten(l):
    return [item for sublist in l for item in sublist]


def get_text(parsed_input):
    return " ".join(
        flatten([[word[1] for word in pgraph[1]] for pgraph in parsed_input if not pgraph[0] == "quote"]))

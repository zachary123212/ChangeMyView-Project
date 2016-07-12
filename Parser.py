from pyparsing import (Suppress, SkipTo, Literal, OneOrMore, Word, ParserElement,
                       StringEnd, printables, Optional, ZeroOrMore)

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

# Ex: this is regular

reg_text = (
    OneOrMore(Word(printables) | Suppress(Literal("\n")) + Word(printables))
    # SkipTo(Literal("*")) | SkipTo(Literal("\n\n"))
).setParseAction(lambda t: [["regular", " ".join(t)]])

text = OneOrMore(bold_italic_text | bold_text | italic_text | reg_text)

# Note: can be either two newlines or the end of the string

line_break = Suppress(
    Literal("\n\n") + ZeroOrMore(Literal("\n")) |
    Literal("\n") + StringEnd() |
    StringEnd()
)

divider = Suppress(OneOrMore(Literal("_")))

paragraph = (
    OneOrMore(text) +
    line_break
).setParseAction(lambda t: [["non-quote", t.asList()]])

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


def flatten(l):
    return [item for sublist in l for item in sublist]


def getText(parsed_input):
    return " ".join(flatten([[word[1] for word in paragraph[1]] for paragraph in parsed_input]))

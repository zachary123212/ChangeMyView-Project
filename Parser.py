from pyparsing import (Suppress, SkipTo, Literal, OneOrMore, Word, ParserElement, StringEnd, printables, Optional,
                       ZeroOrMore, NotAny)

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

link_text = (
    Suppress(Literal("[")) +
    SkipTo(Literal("]")) +
    Suppress(
        Literal("]") +
        Literal("(") +
        SkipTo(Literal(")")) +
        Literal(")")
    )
).setParseAction(lambda t: [["link", t[0]]])

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


def flatten(l):
    return [item for sublist in l for item in sublist]


def get_text(parsed_input):
    return " ".join(flatten([[word[1] for word in paragraph[1]] for paragraph in parsed_input]))

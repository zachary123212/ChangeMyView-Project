from pyparsing import *

italic = Group(Suppress(Literal("*")) + SkipTo(Literal("*")) + Suppress(Literal("*")))
bold = Group(Suppress(Literal("**")) + SkipTo(Literal("**")) + Suppress(Literal("**")))

text = OneOrMore(bold | italic)

print(text.parseString("**this is an bold expression** *this is an italic one*"))



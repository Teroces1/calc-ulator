from enum import Enum

class Tokens(Enum):
    NUMBER = 1
    VARIABLE = 2
    OPERATOR = 3
    LPAREN = 4
    RPAREN = 5
    LITERAL = 6     # for text values that represent mathematical things, such as pi, e, sin, ln, sqrt
    
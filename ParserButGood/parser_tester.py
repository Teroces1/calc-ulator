from parser2 import Parser
from lexer import Lexer
expr="2sin(pi/2)+3.5x-log(10)"
lexer= Lexer(expr)
tokens=lexer.tokenize()
parser=Parser(tokens)
result=parser.parse()
print(result)
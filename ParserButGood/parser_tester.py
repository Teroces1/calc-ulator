from parser import Parser
from lexer import Lexer
expr="2sin(pi/2)+3.5x-log(10)"
expr2="2x=5>=7<9"
lexer= Lexer(expr2)
tokens=lexer.tokenize()
parser=Parser(tokens)
result=parser.parse()
print(result)
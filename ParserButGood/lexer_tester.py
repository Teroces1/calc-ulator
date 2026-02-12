from lexer import Lexer
#expr="2sin(pi/2)+3.5x-log(10)"
expr="2(3x+3)+4"
lexer= Lexer(expr)
tokens=lexer.tokenize()
for token in tokens:
    print(token)
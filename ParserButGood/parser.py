#Shunting Yard parser
from ParserButGood.token import Token 

class Parser:
    def __init__(self, tokens):
        self.tokens=tokens
        self.operator_stack=[]
        self.output_queue=[]
        PRECEDENCE_LEVEL={
            '+':2,
            '-':2,
            '*':3,
            '/':3,
            '^':4
        }

    def shunting_yard(self):
        for token in self.tokens:
            if not isinstance(token, Token):
                continue
            if token.type == "NUMBER":
                self.output_queue.append(token)

    
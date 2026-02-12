#Custom parser directly for custom objects
from ParserButGood.token import Token 
from Datastructures.fraction import Fraction
class Expression: # adding
    def __init__(self, constTerms: list, nonconstTerms: list):
        pass
class Term: #multiplication
    def __init__(self, constTerms: list, nonconstTerms: list):
        pass
class Power:
    def __init__(self, base, exp):
        pass

class Parser2:
    PRECEDENCE = {
            '+':2,
            '-':2,
            '*':3,
            '/':3,
            '^':4
        }
    CONSTANTS= ['e', 'pi']
    def __init__(self, tokens):
        self.tokens=tokens
        self.operator_stack=[]
        self.output_queue=[]
    def peek(self, i):
        return self.tokens[i+1]
    def parse(self):
        for i, token in enumerate(self.tokens):
            if token.type== "NUMBER":
                self.output_queue.append(Fraction(token.value))
            elif token.type=="IDENTIFIER":
                pass
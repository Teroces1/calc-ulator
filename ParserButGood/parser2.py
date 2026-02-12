#Recursive descent parser
from ParserButGood.token import Token 

class AlgebraicNode:
    pass  # added this, but i wont actually be implementing this
    

# these 3 are the main operations
class Expression(AlgebraicNode): #Adding
    def __init__(self, consts, terms):
        self.consts = consts   # is a LIST of AlgebraicNodes
        self.terms = terms     # is a LIST of AlgebraicNodes

class Term(AlgebraicNode): #Multiplication
    def __init__(self, coefs, factors):
        self.coefs = coefs     # is a LIST of AlgebraicNodes
        self.factors = factors # is a LIST of AlgebraicNodes

class Power(AlgebraicNode):
    def __init__(self, base, exp):
        self.base = base       # is a SINGLE AlgebraicNode
        self.exp = exp         # is a SINGLE AlgebraicNode



# this will be used for sin, cos, ln, etc.
class FunctionCall(AlgebraicNode):
    def __init__(self, func, args):
        self.func = func       # will be a string like "sin" or "ln". can also be custom functions like "f" or "f_1"
        self.args = args       # is a LIST of AlgebraicNodes




# the 2 types of base types
class Symbol(AlgebraicNode):  # for variables
    def __init__(self, name):
        self.name = name       # will be a string storing the variables name

class Fraction(AlgebraicNode):
    def __init__(self, numerator, denominator=1):
        self.num = numerator
        self.den = denominator



# Example: in (x-3)/2, the object that containts every other object would be Term
# 2(x+3)+1, the ojbect that containts everything else would be Expression, creating Abstract syntax tree
class Parser:
    PRECEDENCE = {
            '+':2,
            '-':2,
            '*':3,
            '/':3,
            '^':4
        }
    FUNCTIONS={"sin", "cos", "tan", "ln", "log", "sqrt", "abs", "exp"}
    CONSTANTS={"pi", "e"}
    def __init__(self, tokens):
        self.tokens=tokens
        self.pos=0
        self.current_token=''
    def precedence(self, token):
        if isinstance(token, Token):
            return self.PRECEDENCE.get(token.value, -1)
    def left_association(self, token):
        if isinstance(token, Token):
            if token.value != "^":
                return True
            return False
    def peek(self, i):
        return self.tokens[i+1]
    def advance(self):
        self.pos+=1
    def parse_expression(self):
        

        #should return expression object
    def parse_term(self):
        pass
    def parse_power(self):
        pass
    def parse_factor(self):
        pass
        
    def parse(self): #recursive descent parser
        node = self.parse_expression()
        if self.current_token.type == "EOF":
            raise ValueError("Error")
        return node


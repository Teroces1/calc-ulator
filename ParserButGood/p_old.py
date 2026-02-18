#Shunting Yard parser
from ParserButGood.token import Token 

class AlgebraicNode:
    pass  # added this, but i wont actually be implementing this
    

# these 3 are the main operations
class Expression(AlgebraicNode): #Adding
    def __init__(self, consts, terms):
        self.consts = consts   # is a LIST of AlgebraicNodes
        self.terms = terms     # is a LIST of AlgebraicNodes
    def __repr__(self):
        return f"Expression({self.consts}, {self.terms})"
class Term(AlgebraicNode): #Multiplication
    def __init__(self, coefs, factors):
        self.coefs = coefs     # is a LIST of AlgebraicNodes
        self.factors = factors # is a LIST of AlgebraicNodes
    def __repr__(self):
        return f"Term({self.coefs}, {self.factors})"

class Power(AlgebraicNode):
    def __init__(self, base, exp):
        self.base = base       # is a SINGLE AlgebraicNode
        self.exp = exp         # is a SINGLE AlgebraicNode
    def __repr__(self):
        return f"Power({self.base}, {self.exp})"



# this will be used for sin, cos, ln, etc.
class FunctionCall(AlgebraicNode):
    def __init__(self, func, args):
        self.func = func       # will be a string like "sin" or "ln". can also be custom functions like "f" or "f_1"
        self.args = args       # is a LIST of AlgebraicNodes
    def __repr__(self):
        return f"FunctionCall({self.func}, {self.args})"




# the 2 types of base types
class Symbol(AlgebraicNode):  # for variables
    def __init__(self, name):
        self.name = name       # will be a string storing the variables name
    def __repr__(self):
        return f"Symbol({self.name})"

class Fraction(AlgebraicNode):
    def __init__(self, numerator, denominator=1):
        self.num = numerator
        self.den = denominator
    def __repr__(self):
        return f"Fraction({self.num}, {self.den})"
class Equation(AlgebraicNode):
    def __init__(self, expressions):
        self.expr=expressions # arr

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
    def shunting_yard(self):
        for i, token in enumerate(self.tokens):
            if not isinstance(token, Token):
                continue
            if token.type == "NUMBER":
                self.output_queue.append(token)
            elif token.type =="IDENTIFIER":
                nextTok=self.peek(i)
                if nextTok and nextTok.type=="LPAREN":
                    token.type="FUNCTION"
                    self.operator_stack.append(token)
                else: 
                    if token.value in self.CONSTANTS:
                        token.type="CONSTANT"
                        self.output_queue.append(token)
                    else: 
                        token.type="VARIABLE"
                        self.output_queue.append(token)
            elif token.type == "COMMA": 
                # Pop until we find a left parenthesis 
                while self.operator_stack and self.operator_stack[-1].type != "LPAREN": 
                    self.output_queue.append(self.operator_stack.pop()) 
                    # If we never found a left parenthesis, it's an error 
                    if not self.operator_stack: 
                        raise ValueError("Misplaced comma or missing left parenthesis")
            elif token.type=="OPERATOR":
                while (self.operator_stack and self.operator_stack[-1].type=="OPERATOR" and
                       (
                           (self.left_association(token) and 
                            self.precedence(token) <=self.precedence(self.operator_stack[-1]))
                            or 
                            (not self.left_association(token) and
                             self.precedence(token) <self.precedence(self.operator_stack[-1]))
                       )):
                    self.output_queue.append(self.operator_stack.pop())
                self.operator_stack.append(token)
            elif token.type=="LPAREN":
                self.operator_stack.append(token)
            elif token.type=="RPAREN":
                while True:
                    if not self.operator_stack:
                        raise ValueError('Missing left parenthesis')
                    if self.operator_stack[-1].type =="LPAREN":
                        self.operator_stack.pop()
                        break

                self.output_queue.append(self.operator_stack.pop())
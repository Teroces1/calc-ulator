#Recursive descent parser
from ParserButGood.token import Token 

class AlgebraicNode:
    pass  # added this, but i wont actually be implementing this
    

# these 3 are the main operations
class Expression(AlgebraicNode): #Adding
    def __init__(self, consts, terms):
        self.consts = consts   # is a LIST of AlgebraicNodes
        self.terms = terms     # is a LIST of AlgebraicNodes
#Even though terms and consts have different lists, it is implemented in the way that you can just put everything into terms and everything will be sorted out.
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
        self.current_token=tokens[self.pos]
        self.terms=[]
    def precedence(self, token):
        if isinstance(token, Token):
            return self.PRECEDENCE.get(token.value, -1)
    def left_association(self, token):
        if isinstance(token, Token):
            if token.value != "^":
                return True
            return False
    def error(self, message):
        raise ValueError(message)
    def peek(self, i):
        return self.tokens[i+1]
    def advance(self):
        self.pos+=1
        self.current_token=self.tokens[self.pos]
    def is_multiplication_context(self):
        if self.current_token.value in ('*', '/'):
            return True
        
        prev=self.tokens[self.pos-1] if self.pos >0 else None
        curr=self.current_token
        if prev and curr:
            if (
                prev.type=="NUMBER" and curr.type in ("IDENTIFIER", "LPAREN") or
                prev.type=="IDENTIFIER" and curr.type in ("IDENTIFIER", "LPAREN") or
                prev.type=="RPAREN" and curr.type in ("IDENTIFIER", "LPAREN", "NUMBER")
                ):
                return True
        return False
    def is_function(self):
        return (
            self.current_token.type=="IDENTIFIER" and
            self.pos+1<len(self.tokens) and 
            self.tokens[self.pos+1].type=='LPAREN' and 
            self.current_token.value in self.FUNCTIONS
        )
    
    #Start from here
    def parse_expression(self):
        left=[self.parse_term()]
        while self.current_token.value in ('+', '-'):
            op=self.current_token.value
            self.advance()
            right=self.parse_term()
            if op=="-":
                left.append(Term([Fraction(-1)],[right])) #Terms can be nested inside of each other, so its fine
            else:
                left.append(right)
        if len(left)==1:
            return left[0]
        return Expression([], left) #it is fine that const arr is empty, as it will be sorted out further
    
    #Parses terms(multiplication, division, even implicit)
    def parse_term(self):
        left=self.parse_power()
        factors=[left]
        while self.is_multiplication_context():
            op=self.current_token
            if op in ('*', '/'):
                self.advance()
            right=self.parse_power()
            factors.append(right)
        return Term([],factors) 
    def parse_power(self):
        base=self.parse_primary()
        while self.pos+1<len(self.tokens) and self.tokens[self.pos+1].value=="^":
            self.advance()
            self.advance()
            exp=self.parse_power()
            base=Power(base, exp)
        return base
    
    #The lowest level of parsing
    def parse_primary(self):
        if self.current_token.type=="NUMBER":
            node=Fraction(self.current_token.value)
            self.advance()
            return node
        if self.current_token.type=="IDENTIFIER":
            name=self.current_token.value
            if self.current_token.value in self.CONSTANTS:
                node=Symbol(self.current_token.value)
                self.advance()
                return node
            if self.is_function():
                self.advance()
                self.advance()
                args=[self.parse_expression()]
                while self.current_token.type=="COMMA":
                    self.advance()
                    args.append(self.parse_expression())
                if self.current_token.type!="RPAREN":
                    self.error("Expected ')' after func args")
                self.advance()
                return FunctionCall(name, args)
            else: 
                self.advance()
                return Symbol(name)
        if self.current_token.type=="LPAREN" and self.pos+1<len(self.tokens):
            self.advance()
            node=self.parse_expression()
            if self.current_token.type!="RPAREN":
                self.error("Expected ')' after '('")
            self.advance()
            return node
        if self.current_token.value=="-":
            self.advance()
            node = self.parse_primary()
            return Term([Fraction(-1)], [node])
        self.error(f"Couldn't parse token {self.current_token} on a simplest level")

    # The
    def parse(self): #recursive descent parser
        node = self.parse_expression()
        if self.current_token.type == "EOF":
            raise ValueError("Error")
        return node


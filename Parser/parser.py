#Recursive descent parser
from token import Token 
from ghost_classes import AlgebraicNode, Expression,  Term, Power, FunctionCall, Symbol, Fraction

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
            return token.value != "^"
        
    def error(self, message):
        raise ValueError(message)
    
    def peek(self, i):
        return self.tokens[i+1]
    
    def advance(self):
        self.pos+=1
        self.current_token=self.tokens[self.pos]

    def is_explicit(self):
        return self.current_token.value in ('*', '/')
    
    def is_implicit(self):
        if self.pos==0:
            return False
        
        prev=self.tokens[self.pos-1]
        curr=self.current_token
        
        if curr.type=="IDENTIFIER" and self.is_function():
            return prev.type in ("NUMBER", "IDENTIFIER", "RPAREN")
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
        while True:
            explicit=self.is_explicit()
            implicit=self.is_implicit()
            if explicit:
                oper=self.current_token.value
                self.advance()
                right=self.parse_power()
                if oper=="/":
                    factors.append(Power(right, Fraction(-1)))
                else:
                    factors.append(right)
            elif implicit:
                right=self.parse_power()
                factors.append(right)
            else: 
                break
        return Term([],factors) 
    
    #Parses powers and exponents
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
        if self.current_token.type != "EOF":
            raise ValueError("Unexpected token after expression ended")
        return node


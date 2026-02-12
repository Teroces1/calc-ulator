#Shunting Yard parser
from ParserButGood.token import Token 

class Expression:
    def __init__(self, constTerms: list, nonconstTerms: list):
        pass
class Term:
    def __init__(self, constTerms: list, nonconstTerms: list):
        pass
class Power:
    def __init__(self, base, exp):
        pass




# infix to postfix -> 3 + 4 * 2 => 3 4 2 + *
class Parser:
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
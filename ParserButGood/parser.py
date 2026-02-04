#Shunting Yard parser
from ParserButGood.token import Token 
# infix to postfix -> 3 + 4 * 2 => 3 4 2 + *
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
            elif token.type =="FUNCTION":
                self.operator_stack.append(token)
                #todo parentheses logic
            elif token.type == "COMMA": 
                # Pop until we find a left parenthesis 
                while self.operator_stack and self.operator_stack[-1].type != "LPAREN": 
                    self.output_queue.append(self.operator_stack.pop()) 
                    # If we never found a left parenthesis, it's an error 
                    if not self.operator_stack: 
                        raise ValueError("Misplaced comma or missing left parenthesis")
            elif token.type=="OPERATOR":
                return
                #to do

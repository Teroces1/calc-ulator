#Here the tokenizer will split the string into the stuff, like FUNCTION, OPERATOR, NUMBER etc.
FUNCTIONS={"sin", "cos", "tan", "ln", "log", "sqrt", "abs", "exp"}
CONSTANTS={"pi", "e"}
from ParserButGood.token import Token
class Lexer:
    def __init__(self, text):
        self.text=text
        self.pos=0
        self.length=len(text)
    def current_char(self):
        if self.pos>=len(self.text):
            return None
        else:
            return self.text[self.pos]
    def advance(self):
        self.pos+=1
    def peek(self):
        if self.pos+1>=len(self.text):
            return None
        else:
            return self.text[self.pos+1]
    def skip_whitespace(self):
        while self.text[self.pos]==" ":
            self.advance()
    def number(self):
        string = ""
        decimal = ""
        dotCount=0
        while self.current_char() is not None:
            ch=self.current_char()
            if ch.isdigit() and dotCount==0:
                string+=ch
                self.advance()
                continue
            if ch=="." and dotCount==0:
                dotCount+=1
                self.advance()
                continue
            if ch.isdigit() and dotCount==1:
                decimal +=ch
                self.advance()
                continue
            break
        if dotCount==1:
            if string=="":
                string="0"
            return Token("NUMBER", string+"."+decimal)
        else:
            return Token("NUMBER", string)
    def identifier
            
#Here the tokenizer will split the string into the stuff, like FUNCTION, OPERATOR, NUMBER etc.
FUNCTIONS={"sin", "cos", "tan", "ln", "log", "sqrt", "abs", "exp"}
CONSTANTS={"pi", "e"}
from token import Token
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
        while self.current_char()==" ":
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
            if dotCount>1:
                self.error("Ill formed number")
            break
        if dotCount==1:
            if string=="":
                string="0"
            return Token("NUMBER", string+"."+decimal)
        else:
            return Token("NUMBER", string)
    def identifier(self):
        string=""
        ch=self.current_char()
        if not ch.isalpha():
            self.error("First char has to be a letter")
        string+=ch
        self.advance()
        while self.current_char() is not None and self.current_char().isalnum():
            ch=self.current_char()
            string+=ch
            self.advance()
        return Token("IDENTIFIER", string)
    def error(self, message):
        raise Exception(f"Lexer error ar position {self.pos}: {message}")
    def get_next_token(self):
        while self.current_char() is not None:
            ch=self.current_char()
            self.skip_whitespace()
            if ch.isdigit() or ch==".":
                return self.number()
            if ch.isalpha():
                return self.identifier()
            if ch in "*/+-^":
                self.advance()
                return Token("OPERATOR", ch)
            if ch=="(":
                self.advance()
                return Token("LPAREN", ch)
            if ch==")":
                self.advance()
                return Token("RPAREN", ch)
            if ch==",":
                self.advance()
                return Token("COMMA", ch)
            if ch=="_":
                self.advance()
                return Token("UNDERSCORE", ch)
            self.error(f"Unknown character: {ch}")
        return Token("EOF", "")
    def tokenize(self):
        tokens=[]
        while True:
            tok=self.get_next_token()
            tokens.append(tok)
            if tok.type=="EOF": # End of File token
                break
        return tokens
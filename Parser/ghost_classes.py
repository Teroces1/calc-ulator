class AlgebraicNode:
    pass  # added this, but i wont actually be implementing this
    

# these 3 are the main operations
class Expression(AlgebraicNode): #Adding
    def __init__(self, consts, terms):
        self.consts = consts   # is a LIST of AlgebraicNodes
        self.terms = terms     # is a LIST of AlgebraicNodes
    def __repr__(self):
        return f"Expression({self.consts}, {self.terms})"
#Even though terms and consts have different lists, it is implemented in the way that you can just put everything into terms and everything will be sorted out.
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



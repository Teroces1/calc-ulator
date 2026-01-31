import math

class Power:
    __slots__=("base", "exponent")
    def __init__(self, base=0, exp=1):
        self.base=base
        self.exp=exp
    def __handlePowerZero__(self):
        if self.exp==0:
            if self.base==0:
                return "undefined"
            return Power(1, 1)
    def __handlePowerOne__(self):
        if self.exp==1:
            return self.base
    def __handleBaseOne__(self):
        if self.base==1:
            return 1
    def __handleBaseZero__(self):
        if self.base==0:
            if self.exp==0:
                return "undefined"
            elif self.exp<0:
                return "division by zero"
            else:
                return 0
    def __handleNegativeExponent__(self):
        if self.exp <0:
            #I basically want to return Fraction(1, Power(self.base, self.exp))
            return 0
    def __repr__(self):
        return f"Power({self.base}, {self.exponent})"
import math
from Datastructures.fraction import Fraction
class Power:
    __slots__=("base", "exponent")
    def __init__(self, base=0, exp=1):
        self.base=base
        self.exp=exp
    #
    # My own methods
    #
    def copy(self):
        return Power(self.base, self.exp)
    def is_integer(self):
        if ((self.base**self.exp) % math.floor(self.base**self.exp) ) !=0:
            return False
    def _handlePowerZero(self):
        if self.exp==0:
            if self.base==0:
                return "undefined"
            return Fraction(1, 1)
    def _handlePowerOne(self):
        if self.exp==1:
            return Fraction(self.base, 1)
    def _handleBaseOne(self):
        if self.base==1:
            return Fraction(1,1)
    def _handleBaseZero(self):
        if self.base==0:
            if self.exp==0:
                return "undefined"
            elif self.exp<0:
                return "division by zero"
            else:
                return Fraction()
    def _handleNegativeExponent(self):
        if self.exp <0:
            return Fraction(1,Power(self.base, -self.exp))
    def _handleConstantToIntPower(self):
        if isinstance(self.base, Fraction) and isinstance(self.exp, Fraction) and self.exp.den == 1:
            return self.base ** self.exp.num    
        return self
    def _handleVariableToNumberPower(self):
        #todo
        return
    def _handleNumberToVariablePower(self):
        #todo
        return
    def checkForZero(self, power):
        if isinstance(power, Power):
            #to do
            return True
    @classmethod
    def isNumerical(cls, power):
        if isinstance(power, Power):
            return ( isinstance(power.base, (int, float, Fraction)) and isinstance(power.exp, (int, float, Fraction)) )
    #
    # Default python methods
    #
    def __int__(self):
        return math.floor(self.base**self.exp)
    def __round__(self, n=0):
        return round(self.base ** self.exp, n)
    def __bool__(self):
        if self.checkForZero(self): #Need to change so that takes no parameters
            return True
        return False
    
    def __pos__(self):
        return self.copy()
    def __add__(self, other):
        if isinstance(other, Power):
            if self.isNumerical(self) and self.isNumerical(other):
                return #need to return expression here
    def __neg__(self):
        return Power(-self.base, self.exp)
    def __abs__(self):
        return Power(abs(self.base), self.exp)
    def __pow__(self, n):
        return Power(self.base, self.exp*n)
    def __mul__(self, other):
        if isinstance(other, Power):
            if other.base==self.base:
                return Power(self.base, self.exp+other.exp)
        else: 
            return NotImplemented
    def __truediv__(self, other):
        if isinstance(other, Power):
            if not self.checkForZero(other):
                return Power(self.base, self.exp-other.exp)
    def __floor__(self):
        if self.isNumerical(self):
            return Power(math.floor(self.base**self.exp),1)
    def __repr__(self):
        return f"Power({self.base}, {self.exponent})"
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
        return Power(self.base.copy(), self.exp.copy())
    def is_integer(self):
        if isinstance(self.base, (int, float)) and isinstance(self.exp, (int, float)): # Const to the power of const
            if ((self.base**self.exp) % math.floor(self.base**self.exp)) !=0:
                return False
            else:
                return True
        if isinstance(self.base, (int, float)) and isinstance(self.exp, Fraction): # Handles case of constant to the power of fraction
            if (self.base**(self.exp.num/self.exp.den)) % math.floor((self.base**(self.exp.num/self.exp.den))) !=0:
                return False
            else: 
                return True
        if isinstance(self.base, Fraction) and isinstance(self.exp, (int, float)): #Fraction to the power of const
            if ((self.base.num**self.exp)/(self.base.den**self.exp)) % math.floor((self.base.num**self.exp)/(self.base.den**self.exp)) !=0:
                return False
            else: 
                return True
        if isinstance(self.base, Fraction) and isinstance(self.exp, Fraction): #Handles fraction to the power of fraction
            if (((self.base.num/self.base.den)^(self.exp.num/self.base.den)) % math.floor((self.base.num/self.base.den)^(self.exp.num/self.base.den))) !=0:
                return False
            else:
                return True
    def is_const(self):
        return # self.base.is_const() and self.exp.is_const():
    def as_tuple(self):
        return (self.base, self.exp)
    def _handlePowerZero(self):
        if self.is_const():
            if self.exp==0:
                if self.base==0:
                    return "undefined"
                return 1
    def _handlePowerOne(self):
        if self.is_const():
            if self.exp==1:
                return self.base.copy()
    def _handleBaseOne(self):
        if self.is_const():
            if self.base==1:
                return self.base.copy()
    def _handleBaseZero(self):
        if self.is_const():
            if self.base==0:
                if self.exp==0:
                    return "undefined"
                elif self.exp<0:
                    return "division by zero"
                else:
                    return Fraction()
    def _handleNegativeExponent(self):
        if self.is_const(): # Need to check for const cause can't have expressions in Fractions
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
        if self.is_const():
            return math.floor(self.base**self.exp)
        # Just throw an error if try to use int() on a expression?
    def __round__(self, n=0):
        if self.is_const():
            return round(self.base ** self.exp, n)
    def __pos__(self):
        return self.copy()
    def __add__(self, other):
        if isinstance(other, Power):
            if self.isNumerical(self) and self.isNumerical(other):
                if self.base == other.base:
                    return # TODO, Return expressions ex: e^x + e^(x+2) will return e^x(1+e^2)
    def __neg__(self):
        return #todo after multiplying
    def __abs__(self):
        return Power(abs(self.base), self.exp)
    def __pow__(self, n):
        return Power(self.base, self.exp*n) # Might need to change later, when going to have expressions
    def __mul__(self, other):
        if isinstance(other, Power):
            if other.base==self.base:
                return Power(self.base, self.exp+other.exp)
            else: 
                return NotImplemented
        else: 
            return NotImplemented
    def __truediv__(self, other):
        if isinstance(other, Power):
            if not self.checkForZero(other):
                return Power(self.base, self.exp-other.exp)
    def __floor__(self):
        if self.is_const():
            return Power(math.floor(self.base**self.exp),1)
    def __repr__(self):
        return f"Power({self.base}, {self.exponent})"
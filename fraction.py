import math

class Fraction:
    __slots__ = ("num", "den")
    def __setattr__(self, name, value):
        if hasattr(self, name):
            raise AttributeError("Fraction is immutable")
        super().__setattr__(name, value)


    def __init__(self, numerator=0, denominator=1):
        if denominator < 0:
            numerator = -numerator
            denominator = -denominator
        
        f = math.gcd(numerator, denominator)
        numerator //= f
        denominator //= f

        self.num = numerator
        self.den = denominator


    # def simplify(self):
    #     if self.den < 0:
    #         self.num = -self.num
    #         self.den = -self.den
        
    #     f = math.gcd(self.num, self.den)
    #     self.num //= f
    #     self.den //= f
        
    #     return self

    def simplified(self):
        n, d = self.num, self.den
        if d < 0:
            n = -n
            d = -d
        
        f = math.gcd(n, d)
        n //= f
        d //= f
        return Fraction(n, d)
    
    def copy(self):
        return Fraction(self.num, self.den)
    
    def sign(self):
        return 1 if self.num > 0 else -1 if self.num < 0 else 0
    @staticmethod
    def fromFloat(x):
        return Fraction(*x.as_integer_ratio())
    def is_integer(self):
        return self.den == 1
    def as_tuple(self):
        return (self.num, self.den)
    def __int__(self):
        return self.num // self.den
    def __round__(self, n=0):
        return round(self.num / self.den, n)
    def __bool__(self):
        return self.num != 0

    def __pos__(self):  # quick way to make a copy
        return self.copy()
    def __neg__(self):
        return Fraction(-self.num, self.den)
    def __abs__(self):
        return Fraction(abs(self.num), abs(self.den))

    def __add__(self, other):
        if isinstance(other, Fraction):
            return Fraction(self.num * other.den + other.num * self.den, self.den * other.den)
        elif isinstance(other, int):
            return Fraction(self.num + other * self.den, self.den)
        return NotImplemented
    def __radd__(self, other):
        return self.__add__(other)
    
    def __mul__(self, other):
        if isinstance(other, Fraction):
            return Fraction(self.num * other.num, self.den * other.den)
        elif isinstance(other, int):
            return Fraction(self.num * other, self.den)
        return NotImplemented
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __sub__(self, other):
        if isinstance(other, Fraction):
            return Fraction(self.num * other.den - other.num * self.den, self.den * other.den)
        elif isinstance(other, int):
            return Fraction(self.num - other * self.den, self.den)
        return NotImplemented
    def __rsub__(self, other):
        if isinstance(other, Fraction):
            return Fraction(other.num * self.den - self.num * other.den, self.den * other.den)
        elif isinstance(other, int):
            return Fraction(other * self.den - self.num, self.den)
        return NotImplemented
    
    def __truediv__(self, other):
        if isinstance(other, Fraction):
            if other.num == 0:
                raise ZeroDivisionError()
            return Fraction(self.num * other.den, self.den * other.num)
        elif isinstance(other, int):
            if other == 0:
                raise ZeroDivisionError()
            return Fraction(self.num, self.den * other)
        return NotImplemented
    def __rtruediv__(self, other):
        if self.num == 0:
            raise ZeroDivisionError()
        if isinstance(other, Fraction):
            return Fraction(self.den * other.num, self.num * other.den)
        elif isinstance(other, int):
            return Fraction(self.den * other, self.num)
        return NotImplemented
    
    def __pow__(self, n):
        if not isinstance(n, int):
            return NotImplemented
        if n >= 0:
            return Fraction(self.num**n, self.den**n)
        else:
            return Fraction(self.den**(-n), self.num**(-n))

    

    # def __iadd__(self, other):
    #     if isinstance(other, Fraction):
    #         self.num = self.num * other.den + other.num * self.den
    #         self.den *= other.den
    #         self.simplify()
    #     elif isinstance(other, int):
    #         self.num += other * self.den
    #         self.simplify()
    #     else:
    #         return NotImplemented
        
    #     return self
    # def __isub__(self, other):
    #     if isinstance(other, Fraction):
    #         self.num = self.num * other.den - other.num * self.den
    #         self.den *= other.den
    #         self.simplify()
    #     elif isinstance(other, int):
    #         self.num -= other * self.den
    #         self.simplify()
    #     else:
    #         return NotImplemented
        
    #     return self
    # def __imul__(self, other):
    #     if isinstance(other, Fraction):
    #         self.num *= other.num
    #         self.den *= other.den
    #         self.simplify()
    #     elif isinstance(other, int):
    #         self.num *= other
    #         self.simplify()
    #     else:
    #         return NotImplemented
        
    #     return self
    # def __itruediv__(self, other):
    #     if isinstance(other, Fraction):
    #         if other.num == 0:
    #             raise ZeroDivisionError()
    #         self.num *= other.den
    #         self.den *= other.num
    #         self.simplify()
    #     elif isinstance(other, int):
    #         if other == 0:
    #             raise ZeroDivisionError()
    #         self.den *= other
    #         self.simplify()
    #     else:
    #         return NotImplemented
        
    #     return self
    

    def __floor__(self):
        whole = self.num // self.den
        return Fraction(whole, 1)
    def __ceil__(self):
        q, r = divmod(self.num, self.den)
        return Fraction(q if r == 0 else q + 1, 1)
    
    def __trunc__(self):
        return self.num // self.den
    def __complex__(self):
        return complex(self.num / self.den)
    
    def __eq__(self, other):
        if isinstance(other, Fraction):
            return self.num * other.den == other.num * self.den
        if isinstance(other, int):
            return self.num == other * self.den
        
        return NotImplemented
    def __ne__(self, other):
        eq = self.__eq__(other)
        if eq is NotImplemented:
            return NotImplemented
        return not eq
    
    def __lt__(self, other):
        if isinstance(other, Fraction):
            return self.num * other.den < other.num * self.den
        if isinstance(other, int):
            return self.num < other * self.den
        
        return NotImplemented
    def __le__(self, other):
        if isinstance(other, Fraction):
            return self.num * other.den <= other.num * self.den
        if isinstance(other, int):
            return self.num <= other * self.den
        
        return NotImplemented
    def __gt__(self, other):
        if isinstance(other, Fraction):
            return self.num * other.den > other.num * self.den
        if isinstance(other, int):
            return self.num > other * self.den
        
        return NotImplemented
    def __ge__(self, other):
        if isinstance(other, Fraction):
            return self.num * other.den >= other.num * self.den
        if isinstance(other, int):
            return self.num >= other * self.den
        
        return NotImplemented
    

    def __float__(self):
        return self.num / self.den
    
    def __str__(self):
        if self.den == 1:
            return f"({self.num})"
        return f"({self.num}/{self.den})"
    def __repr__(self):
        return f"Fraction({self.num}, {self.den})"
    
    def __hash__(self):
        return hash((self.num, self.den))
    
    def __iter__(self):
        yield self.num
        yield self.den
        
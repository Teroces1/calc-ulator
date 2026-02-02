from Datastructures.fraction import Fraction


class Expression:
    __slots__ = ("const", "terms")
    def __setattr__(self, name, value):
        if hasattr(self, name):
            raise AttributeError("Variable is immutable")
        super().__setattr__(name, value)



    def __init__(self, const, terms):
        self.const = const
        self.terms = terms

    # takes a list of terms, containing a mix of constants and non-constants
    def _sortTerms(self, oldterms):
        consts = []
        terms = []
        for v in oldterms:
            if v.isConstant():
                consts.append(v)
            else:
                terms.append(v)
        
        terms.sort(key = hash)

        return consts, terms
    
    def _foldConsts(self, consts):
        pass
            

    def simplified(self):
        oldterms = []
        for v in self.terms:
            oldterms.append(v.simplified())
            
        # simplification logic here
        #
        # ex:
        # Expression("..a..") + Expression("..b..") - Expression("..a..") -> Variable("..b..")
        # Variable("a") + Fraction(0) -> Variable("a")
        # Fraction(5) + Fraction(9) + Fraction(3) -> Fraction(17)
        pass


    def rewrite(self, rule):
        # rewrite the expression based on the rule
        pass


    def isConstant(self):
        # returns true if all parts of the expression are constants
        # 5 + 3 + sqrt(2) returns true
        # 5*x + 3 + 9 returns false because of the "x" variable
        for v in self.terms:
            if not v.isConstant():
                return False
        
        return True


    def __str__(self):
        s = ""
        for i, t in enumerate(self.terms):
            s += str(t)
            if i < len(self.terms)-1:
                s += " + "
        return s
    
    def __repr__(self):
        return f"Expression({repr(self.const)}, [{", ".join((repr(v) for v in self.terms))}])"
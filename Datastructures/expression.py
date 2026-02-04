from Datastructures.fraction import Fraction
from Datastructures.forms import ExpressionForm, TermForm, Form, CanonicalForm
# each datastructure *MUST* have
#   simplified() -> returns simplified copy factor first
#   rewrite(rule) -> returns a copy with the given rule applied. if the rule cant be applied, returns as is
#   isConstant() -> returns if the expression is of constant value

class Negate:
    __slots__ = ("expr")
    def __setattr__(self, name, value):
        if hasattr(self, name):
            raise AttributeError("Variable is immutable")
        super().__setattr__(name, value)



    def __init__(self, expr):
        self.expr = expr

    def simplified(self, resultform: ExpressionForm = CanonicalForm):
        expr = self.expr.simplified()

        if isinstance(expr, Negate):
            return expr.expr
        
        if isinstance(expr, Expression) and resultform.expressionForm == ExpressionForm.DISTRIBUTED:
            for v in expr.terms:
                

        return Negate(expr)



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
    
    # takes a list of terms, and tries to elimate any cases of [x + (-x)]
    def _removePairs(self, terms):
        i = 0
        new = []
        while i < len(terms):
            for j in range(i+1, len(terms)):

    
    def _foldConsts(self, consts):
        for i in range(len(consts)):
            consts[i] = consts[i].rewrite(ExpressionForm.Factored)
        
        fractions = []
        complexTerms = []

        for v in consts
            

    def simplified(self, resultform: ExpressionForm = CanonicalForm):
        # first simplify all children
        oldtermsI = [self.const]
        for v in self.terms:
            res = v.simplified(ExpressionForm.Distributed)
            if isinstance(res, Expression):
                oldtermsI.append(res.const)
                for j in res.terms:
                    oldtermsI.append(j)
            else:
                oldtermsI.append(res)
        
        newConsts, newTerms = self._sortTerms()
            
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
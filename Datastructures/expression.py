from Datastructures.fraction import Fraction
from Datastructures.forms import ExpressionForm, TermForm, Form, CanonicalForm, SortOrder
# each datastructure *MUST* have
#   simplified() -> returns simplified copy factor first
#   rewrite(rule) -> returns a copy with the given rule applied. if the rule cant be applied, returns as is
#   isConstant() -> returns if the expression is of constant value


# class Negate:
#     __slots__ = ("expr")
#     def __setattr__(self, name, value):
#         if hasattr(self, name):
#             raise AttributeError("Negate is immutable")
#         super().__setattr__(name, value)



#     def __init__(self, expr):
#         self.expr = expr

#     def simplified(self, resultform: ExpressionForm = CanonicalForm):
#         expr = self.expr.simplified()

#         if isinstance(expr, Negate):
#             return expr.expr
        
#         if isinstance(expr, Expression) and resultform.expressionForm == ExpressionForm.DISTRIBUTED:
#             newTerms = []
#             for v in expr.terms:
#                 newTerms.append(Negate(v))
            
#             return Expression(Negate(expr.const), newTerms).simplified(resultform)

#         return Negate(expr)

# class Inverse:
#     __slots__ = ("expr")
#     def __setattr__(self, name, value):
#         if hasattr(self, name):
#             raise AttributeError("Inverse is immutable")
#         super().__setattr__(name, value)


#     def __init__(self, expr):
#         self.expr = expr

#     def simplified(self, resultform: ExpressionForm = CanonicalForm):
#         expr = self.expr.simplified()

#         if isinstance(expr, Inverse):
#             return expr.expr
#         if isinstance(expr, Negate):
#             if isinstance(expr.expr, Inverse):
#                 return Negate(expr.expr.expr)
#             return Negate(Inverse(expr.expr))   # negate always goes on outside
        
#         if isinstance(expr, Term) and resultform.termForm == TermForm.SPLIT_POWERS:
#             newFactors = []
#             for v in expr.factors:
#                 newFactors.append(Inverse(v))
            
#             return Term(Inverse(expr.coefs), newFactors).simplified(resultform)
        
#         if isinstance(expr, Power):
#             return Power(expr.base, Negate(expr.Power))

#         return Inverse(expr)






class Expression:
    __slots__ = ("consts", "terms")
    def __setattr__(self, name, value):
        if hasattr(self, name):
            raise AttributeError("Expression is immutable")
        super().__setattr__(name, value)



    def __init__(self, consts, terms):
        self.consts = consts
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
        inverses = []
        for v in terms:
            inverses.append(Term(Fraction(-1), v).simplified())
        new = []
        i = 0
        while i < len(terms):
            for j in range(i+1, len(terms)):
                if terms[i] == inverses[j]:
                    del terms[i]
                    del inverses[j]
                    break
            else:
                i += 1
        
        return terms
                
    # MAIN METHOD for folding all constants. tries to simplify as much as possible, keeping the result in distributed form.
    def _foldConsts(self, consts):
        
        fractionalConst = Fraction(0)
        complexTerms = []

        for v in consts:
            if isinstance(v, Fraction):
                fractionalConst += v
            else:
                complexTerms.append(v)
        
        # now, it will factor the result
        factors = []
        
        for i in range(len(complexTerms)):
            complexTerms[i] = complexTerms[i].rewrite(ExpressionForm.Factored)
            if isinstance(complexTerms[i], Term):
                factors[i] = sorted(complexTerms[i].factors + complexTerms[i].coefs, key = lambda expr: expr.getSortOrder())
            else:
                factors[i] = complexTerms[i]
        


        for _ in range(1000): # replace with while True later        
            for i, exp in enumerate(factors):
                for j in range(i+1, len(factors)):
                    
        else:
            print("uh ohhhh, this wasnt supposed to happen!!! >:D")




    def simplified(self, resultform: ExpressionForm = CanonicalForm):
        # first simplify all children
        oldtermsI = []
        for v in self.consts:
            res = v.simplified(ExpressionForm.Distributed)
            if isinstance(res, Expression):
                for j in res.consts:
                    oldtermsI.append(j)
                for j in res.terms:
                    oldtermsI.append(j)
            else:
                oldtermsI.append(res)
        for v in self.terms:
            res = v.simplified(ExpressionForm.Distributed)
            if isinstance(res, Expression):
                for j in res.consts:
                    oldtermsI.append(j)
                for j in res.terms:
                    oldtermsI.append(j)
            else:
                oldtermsI.append(res)
        
        newConsts, newTerms = self._sortTerms(oldtermsI)
            
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

    def getSortOrder(self):
        return (SortOrder.Expression, self.__str__())

    def __str__(self):
        s = ""
        for i, t in enumerate(self.terms):
            s += str(t)
            if i < len(self.terms)-1:
                s += " + "
        return s
    
    def __repr__(self):
        return f"Expression({", ".join((repr(v) for v in self.consts))}, [{", ".join((repr(v) for v in self.terms))}])"

class Term:
    pass

class Power:
    pass
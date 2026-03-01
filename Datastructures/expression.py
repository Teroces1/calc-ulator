from Datastructures.fraction import Fraction
from Datastructures.forms import ExpressionForm, TermForm, Form, CanonicalForm, SortOrder
from Datastructures.symbol import Symbol
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
    __slots__ = ("consts", "terms", "_isConstant", "_sortOrder")
    def __setattr__(self, name, value):
        if hasattr(self, name):
            raise AttributeError("Expression is immutable")
        super().__setattr__(name, value)



    def __init__(self, consts, terms):
        object.__setattr__(self, 'consts', tuple(consts))
        object.__setattr__(self, 'terms', tuple(terms))

    # takes a list of terms, containing a mix of constants and non-constants
    def _sortTerms(self, oldterms):
        consts = []
        terms = []
        for v in oldterms:
            if v.isConstant():
                consts.append(v)
            else:
                terms.append(v)
        
        terms.sort(key = lambda expr: expr.getSortOrder())

        return consts, terms
    
    # takes a list of terms, and tries to elimate any cases of [x + (-x)]
    # this is prob not useful and will prob delete. combine like terms already takes care of this
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
        registry = {}   # use a hashmap
        
        for term in complexTerms:
            if isinstance(term, Term):
                # the term should already be factored AND sorted from a previous simplification step
                # all factors should be in term.coefs, since they are all constants

                # signature will be the irrational (non Fraction() part)
                signature = []
                constant = Fraction(1)
                for v in term.coefs:
                    if isinstance(v, Fraction):
                        constant = v # there should ONLY BE 1, since term already got simplified so all Fractions were folded into 1
                    else:
                        signature.append(v)

                signature = tuple(signature) # packing them into a tuple
                
            else:
                # the term IS NOT a fraction, so it must be an unsimplified Power or FunctionCall or constant Symbol
                signature = (term,)
                constant = Fraction(1)

            if signature not in registry:
                registry[signature] = []
            
            registry[signature].append(constant)

        finalTerms = [fractionalConst]
        for signature, coefsSum in registry.items():
            # Sum the coefficients: [2, sqrt(5), 3] -> Expression(5 + sqrt(5))
            new_coef = Expression(coefsSum, []).simplified() # will fold constants in the coef
            
            if new_coef == 0: 
                continue

            finalTerms.append(Term([new_coef], list(signature)).simplified())   # Term.simplified will distribute any unsimplified combine like terms opperation

        return finalTerms

    def _combineLikeTerms(self, nonConstTerms):
        registry = {}   # use a hashmap
        
        for term in nonConstTerms:
            if isinstance(term, Term):
                # the term should already be factored AND sorted from a previous simplification step
                signature = tuple(term.factors)
                if len(term.coefs) == 1:
                    constant = term.coefs[0]
                else:
                    constant = Term(term.coefs, [])   # will be a list of constant expressions
            else:
                signature = (term,)
                constant = Fraction(1)

            if signature not in registry:
                registry[signature] = []
            
            registry[signature].append(constant)

        finalTerms = []
        for signature, coefsSum in registry.items():
            # Sum the coefficients: [2, sqrt(5), 3] -> Expression(5 + sqrt(5))
            new_coef = Expression(coefsSum, []).simplified() # will fold constants in the coef
            
            if new_coef == 0: 
                continue

            finalTerms.append(Term([new_coef], list(signature)).simplified())

        return finalTerms

        


    def simplified(self, resultform: ExpressionForm = CanonicalForm):
        # first simplify all children
        oldtermsI = []
        for v in self.consts:
            res = v.simplified()
            if isinstance(res, Expression):
                oldtermsI.extend(res.consts)
                oldtermsI.extend(res.terms)
            else:
                oldtermsI.append(res)
        for v in self.terms:
            res = v.simplified()
            if isinstance(res, Expression):
                oldtermsI.extend(res.consts)
                oldtermsI.extend(res.terms)
            else:
                oldtermsI.append(res)
        
        newConsts, newTerms = self._sortTerms(oldtermsI)

        newConsts = self._foldConsts(newConsts)

        newTerms = self._combineLikeTerms(newTerms)

        # TODO: apply rules like sin^2 + cos^2 = 1 and stuff

        # now that Expression has been flattened, sorted, simplified, and distributed, flatten the result one last time
        finalConsts = []
        for v in newConsts:
            if isinstance(v, Expression):
                for j in v.consts:
                    finalConsts.append(j)
            else:
                finalConsts.append(v)
        finalTerms = []
        for v in newTerms:
            if isinstance(v, Expression):
                for j in v.consts:
                    finalTerms.append(j)
                for j in v.terms:
                    finalTerms.append(j)
            else:
                finalTerms.append(v)
        

        if len(finalConsts) == 0 and len(finalTerms) == 0:
            return Fraction(0)
        elif len(finalConsts) == 1 and len(finalTerms) == 0:
            return finalConsts[0]
        elif len(finalTerms) == 1 and len(finalConsts) == 0:
            return finalTerms[0]
        
        return Expression(finalConsts, finalTerms)

            
        

        


    def rewrite(self, rule):
        # rewrite the expression based on the rule
        # not sure if this will be needed yet, leaving it unimplemented
        pass


    def isConstant(self):
        # returns true if all parts of the expression are constants
        # 5 + 3 + sqrt(2) returns true
        # 5*x + 3 + 9 returns false because of the "x" variable

        if hasattr(self, "_isConstant"):
            return self._isConstant
        
        for v in self.terms:
            if not v.isConstant():
                self._isConstant = False
                return False
        
        object.__setattr__(self, "_isConstant", is_const)
        return True

    def getSortOrder(self):
        if hasattr(self, "_sortOrder"):
            return self._sortOrder
        object.__setattr__(self, "_isConstant", (SortOrder.Expression, self.__str__()))
        return self._sortOrder

    def __str__(self):
        s = "("
        total = self.consts + self.terms
        for i, t in enumerate(total):
            s += str(t)
            if i < len(total)-1:
                s += " + "
        return s + ")"
    
    def __repr__(self):
        return f"Expression({", ".join((repr(v) for v in self.consts))}, [{", ".join((repr(v) for v in self.terms))}])"

class Term:
    __slots__ = ("coefs", "factors", "_isConstant", "_sortOrder")
    def __setattr__(self, name, value):
        if hasattr(self, name):
            raise AttributeError("Term is immutable")
        super().__setattr__(name, value)



    def __init__(self, coefs, factors):
        self.coefs = coefs
        self.factors = factors


    def _sortFactors(self, oldFactors):
        coefs = []
        factors = []
        for v in oldFactors:
            if v.isConstant():
                coefs.append(v)
            else:
                factors.append(v)
        
        coefs.sort(key = lambda expr: expr.getSortOrder())
        factors.sort(key = lambda expr: expr.getSortOrder())

        return coefs, factors
    
    def simplified(self, resultform: ExpressionForm = CanonicalForm):
        # first simplify all children
        oldfactorsI = []
        for v in self.coefs:
            res = v.simplified()
            if isinstance(res, Term):
                for j in res.coefs:
                    oldfactorsI.append(j)
                for j in res.factors:
                    print("UH OH, HOW DID THIS HAPPEN? why is there a non constant in a constant")
                    raise RuntimeError
            else:
                oldfactorsI.append(res)
        for v in self.factors:
            res = v.simplified()
            if isinstance(res, Term):
                for j in res.coefs:
                    oldfactorsI.append(j)
                for j in res.factors:
                    oldfactorsI.append(j)
            else:
                oldfactorsI.append(res)
        
        newConsts, newTerms = self._sortFactors(oldfactorsI)

        # TODO: this is just very basic simplification for now.
        return Term(newConsts, newTerms)
    
    def isConstant(self):
        if hasattr(self, "_isConstant"):
            return self._isConstant
        
        for v in self.factors:
            if not v.isConstant():
                self._isConstant = False
                return False
        
        self._isConstant = True
        return True

    def getSortOrder(self):
        if hasattr(self, "_sortOrder"):
            return self._sortOrder
        self._sortOrder = (SortOrder.Term, self.__str__())
        return self._sortOrder

    def __str__(self):
        s = "("
        total = self.coefs + self.factors
        for i, t in enumerate(total):
            s += str(t)
            if i < len(total)-1:
                s += " * "
        return s + ")"
    
    def __repr__(self):
        return f"Term({", ".join((repr(v) for v in self.coefs))}, [{", ".join((repr(v) for v in self.factors))}])"

class Power:
    pass
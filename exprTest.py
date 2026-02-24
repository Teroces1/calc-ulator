from Datastructures.expression import Fraction, Expression, Term, Symbol


e1 = Expression([], [Term([], [Symbol("e"), Symbol("x")]), Term([], [Fraction(2),Symbol("x")])])

print(e1)

e2 = e1.simplified()

print(e2)
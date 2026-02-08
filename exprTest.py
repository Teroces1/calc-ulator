from Datastructures.expression import Fraction, Expression, Term, Symbol


term = Term([Fraction(2)], [Symbol("x"), Symbol("y")])
term2 = Term([Fraction(-4)], [Symbol("y"), Symbol("x")])
e1 = Expression([Fraction(2)], [Fraction(3), term, term2])

print(e1)

e2 = e1.simplified()

print(e2)
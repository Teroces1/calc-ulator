from enum import Enum

class ExpressionForm(Enum):
    DISTRIBUTED = 1,    # 3*x + 3*y
    FACTORED = 2,       # 3*(x + y)

class TermForm(Enum):
    SPLIT_POWERS = 1,   # x^3 * y^3
    GROUP_POWERS = 2    # (x * y)^3

class Form:
    __slots__ = ("expressionForm", "termForm")
    def __setattr__(self, name, value):
        if hasattr(self, name):
            raise AttributeError("Variable is immutable")
        super().__setattr__(name, value)

    def __init__(self, expressionForm: ExpressionForm = ExpressionForm.DISTRIBUTED, termForm = TermForm.SPLIT_POWERS):
        self.expressionForm = expressionForm
        self.termForm = termForm


CanonicalForm = Form()




class SortOrder(Enum):
    Number = 1,
    Symbol = 2,
    Power = 3,
    Term = 4,
    Expression = 5,
    Function = 6,
    Other = 7,

from enum import Enum

class ExpressionForm(Enum):
    FACTORED = 1,
    DISTRIBUTED = 2

class TermForm(Enum):
    Def = 1

class Form:
    __slots__ = ("expressionForm", "termForm")
    def __setattr__(self, name, value):
        if hasattr(self, name):
            raise AttributeError("Variable is immutable")
        super().__setattr__(name, value)

    def __init__(self, expressionForm: ExpressionForm = ExpressionForm.DISTRIBUTED, termForm = TermForm.Def):
        self.expressionForm = expressionForm
        self.termForm = termForm


CanonicalForm = Form()
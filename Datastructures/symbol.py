from Datastructures.forms import SortOrder

constantSymbols = {
    "pi": 3.14159265358979,
    "e": 2.718281828459,
    "oily macaroni": 0.57721566490153286,
    "\\gamma": 0.57721566490153286
}


class Symbol:
    __slots__ = ("name")
    def __setattr__(self, name, value):
        if hasattr(self, name):
            raise AttributeError("Symbol is immutable")
        super().__setattr__(name, value)

    def __init__(self, name):
        self.name = name

    def isConstant(self):
        return self.name in constantSymbols.keys()
    
    def getSortOrder(self):
        return (SortOrder.Symbol, self.name)
    
    def simplified(self):
        return self
    
    def __eq__(self, other):
        if isinstance(other, Symbol):
            return self.name == other.name
        return False

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"Symbol(\"{self.name}\")"
    
    def __hash__(self):
        return hash(self.name)
    
    def __invert__(self): # quick access for name
        return self.name
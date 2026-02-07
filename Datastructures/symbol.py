class Symbol:
    __slots__ = ("name")
    def __setattr__(self, name, value):
        if hasattr(self, name):
            raise AttributeError("Symbol is immutable")
        super().__setattr__(name, value)

    def __init__(self, name):
        self.name = name

    def isConstant(self):
        return False

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"Symbol(\"{self.name}\")"
    
    def __hash__(self):
        return hash(self.name)
    
    def __invert__(self): # quick access for name
        return self.name
class Token:
    __slots__=("type", "value")
    def __init(self, type, value):
        self.type=type
        self.value=value
    def __repr__(self):
        return f"Token of type {self.type} and value {self.value}"
    


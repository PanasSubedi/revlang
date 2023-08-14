class Token:
    def __init__(self, token_type: str, token_value: str) -> None:
        self.type = token_type
        self.value = token_value

    def __repr__(self) -> str:
        return f"<{self.type} {self.value}>"

class Declaration(Token):
    def __init__(self, token_value: str) -> None:
        super().__init__("DECL", token_value)

class Variable(Token):
    def __init__(self, token_value: str) -> None:
        super().__init__("VAR(?)", token_value)

class VariableSeparator(Token):
    def __init__(self) -> None:
        super().__init__("SEP", None)

class StatementEnder(Token):
    def __init__(self) -> None:
        super().__init__("END", None)

class Operator(Token):
    def __init__(self, token_value: str) -> None:
        super().__init__("OP", token_value)

class Integer(Token):
    def __init__(self, token_value: str) -> None:
        super().__init__("INT", token_value)

class Float(Token):
    def __init__(self, token_value: str) -> None:
        super().__init__("FLT", token_value)
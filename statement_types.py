class StatementType:
    def __init__(self, type) -> None:
        self.type = type

    def __repr__(self) -> str:
        return f"<StatementType {self.type}>"
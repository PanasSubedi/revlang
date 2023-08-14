class Parser:
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.index = 0
        self.current_token = self.tokens[self.index]

    def variable(self) -> None:
        if self.current_token.type.startswith("VAR"):
            return self.current_token

    def statement(self) -> list:
        if self.current_token.type == "DECL":
            variables = []
            declaration_token = self.current_token
            while self.index < len(self.tokens) and self.current_token.type != "END":
                self.forward()
                variables.append(self.variable())
                self.forward()
            return [declaration_token, variables]
        
    def parse(self) -> list:
        return self.statement()
    
    def forward(self) -> None:
        self.index += 1
        if self.index < len(self.tokens):
            self.current_token = self.tokens[self.index]
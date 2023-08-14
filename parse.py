class Parser:
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.index = 0
        self.current_token = self.tokens[self.index]

    def variable(self) -> None:
        if self.current_token.type.startswith("VAR"):
            return self.current_token
        
    def factor(self):
        if self.current_token.type in ("FLT", "INT"):
            return self.current_token
        elif self.current_token.type.startswith("VAR"):
            return self.current_token
        
    def assignment_expression(self) -> list:
        left_node = self.factor()
        self.forward()
        
        while self.current_token.value == "=":
            operator = self.current_token
            self.forward()
            right_node = self.factor()
            left_node = [left_node, operator, right_node]
        return left_node

    def statement(self) -> list:
        if self.current_token.type == "DECL":
            variables = []
            declaration_token = self.current_token
            while self.index < len(self.tokens) and self.current_token.type != "END":
                self.forward()
                variables.append(self.variable())
                self.forward()
            return [declaration_token, variables]
        
        elif self.current_token.type in ("INT", "FLT", "OP") or self.current_token.type.startswith("VAR"):
            return self.assignment_expression()
        
    def parse(self) -> list:
        return self.statement()
    
    def forward(self) -> None:
        self.index += 1
        if self.index < len(self.tokens):
            self.current_token = self.tokens[self.index]
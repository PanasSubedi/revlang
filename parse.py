from tokens import Variable, Operator

class Parser:
    REVERSE_OPERATORS = {
        "+": "-",
        "-": "+",
        "*": "/",
        "/": "*"
    }
    
    def __init__(self, tokens, direction=1, statement_type=None) -> None:
        self.tokens = tokens
        self.index = 0
        self.current_token = self.tokens[self.index]
        self.direction = direction
        self.statement_type = statement_type
        self.update_variable = None

    def variable(self) -> None:
        if self.current_token.type.startswith("VAR"):
            return self.current_token
        
    def factor(self):
        if self.current_token.type in ("FLT", "INT"):
            return self.current_token
        elif self.current_token.value == "(":
            self.forward()
            expression = self.assignment_expression()
            return expression
        elif self.current_token.value == "not":
            operator = self.current_token
            self.forward()
            return [operator, self.assignment_expression()]
        elif self.current_token.type.startswith("VAR"):
            return self.current_token
        elif self.current_token.value in ("+", "-"):
            operator = self.current_token
            self.forward()
            operand = self.assignment_expression()

            return [operator, operand]
        
    def term(self):
        left_node = self.factor()
        self.forward()

        while self.current_token.value in ("*", "/"):
            operator = self.current_token
            self.forward()
            right_node = self.factor()
            self.forward()

            if self.direction == 0 and self.statement_type.type == "update" and \
                ((isinstance(left_node, Variable) and left_node.value == self.update_variable.value) or \
                 (isinstance(right_node, Variable) and right_node.value == self.update_variable.value)):
                operator = Operator(Parser.REVERSE_OPERATORS.get(operator.value))

            left_node = [left_node, operator, right_node]

        return left_node
        
    def expression(self) -> list:
        left_node = self.term()

        while self.current_token.value in ("+", "-"):
            operator = self.current_token
            self.forward()
            right_node = self.term()

            if self.direction == 0 and self.statement_type.type == "update" and \
                ((isinstance(left_node, Variable) and left_node.value == self.update_variable.value) or \
                 (isinstance(right_node, Variable) and right_node.value == self.update_variable.value)):
                operator = Operator(Parser.REVERSE_OPERATORS.get(operator.value))

            left_node = [left_node, operator, right_node]

        return left_node
    
    def boolean_expression(self) -> list:
        left_node = self.expression()
        while self.current_token.value in ("and", "or"):
            operator = self.current_token
            self.forward()
            right_node = self.expression()
            left_node = [left_node, operator, right_node]
        return left_node
    
    def comparison_expression(self) -> list:
        left_node = self.boolean_expression()
        while self.current_token.type == "CMP":
            operator = self.current_token
            self.forward()
            right_node = self.boolean_expression()
            left_node = [left_node, operator, right_node]
        return left_node
        
    def assignment_expression(self) -> list:
        left_node = self.comparison_expression()
        
        while self.current_token.value == "=":
            if isinstance(left_node, Variable) and self.statement_type.type == "update":
                self.update_variable = left_node

            operator = self.current_token
            self.forward()
            right_node = self.comparison_expression()
            left_node = [left_node, operator, right_node]

        return left_node
    
    def separated_expression(self) -> list:
        if self.current_token.type == "SEP":
            left = self.current_token
            self.forward()
            mid = self.assignment_expression()
            right = self.current_token
            return [left, mid, right]
        
        return self.assignment_expression()
    
    def if_statement(self) -> list:
        self.forward()
        condition = self.comparison_expression()

        if self.current_token.value == "{":
            self.forward()
            action = self.statement()
            return condition, action
        elif self.tokens[self.index-1].value == "{":
            action = self.statement()
            return condition, action
    
    def if_statement(self) -> list:
        if self.current_token.value in ("if", "elif"):
            self.forward()
            return self.comparison_expression()
        else:
            return []
    
    def while_statement(self) -> list:
        self.forward()
        return self.comparison_expression()
    
    def print_statement(self) -> list:
        self.forward()
        print_variable = self.comparison_expression()
        return print_variable if isinstance(print_variable, list) == 1 else [print_variable,]

    def statement(self) -> list:
        if self.current_token.type == "DECL":
            variables = []
            declaration_token = self.current_token
            while self.index < len(self.tokens) and self.current_token.type != "END":
                self.forward()
                variables.append(self.variable())
                self.forward()
            return [declaration_token, variables]
        
        elif self.current_token.value == "print":
            return [self.current_token, self.print_statement()]
        
        elif self.current_token.value in ("if", "elif", "else"):
            return [self.current_token, self.if_statement()]
        
        elif self.current_token.value == "while":
            return [self.current_token, self.while_statement()]
        
        #elif self.current_token.type in ("INT", "FLT", "OP") or self.current_token.type.startswith("VAR") or self.current_token.value == "not":
        else:
            return self.separated_expression()
        
    def parse(self) -> list:
        statement = self.statement()
        if not isinstance(statement, list):
            return [statement,]
        else:
            return statement
    
    def forward(self) -> None:
        self.index += 1
        if self.index < len(self.tokens):
            self.current_token = self.tokens[self.index]
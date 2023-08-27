from tokens import Declaration, Variable, VariableSeparator,\
    Operator, Integer, Float, BooleanOperator,\
    ComparisonOperator, Keyword, Separator
from statement_types import StatementType


from error import Error

class Lexer:

    NUMBERS = "0123456789"
    LETTERS = "abcdefghijklmnopqrstuvwxyz"
    VALID_VARIABLE_CHARACTERS = LETTERS + NUMBERS + "_"
    OPERATORS = "=+-*/()"
    STOP_WORDS = [" ", "}"]
    DECLARATIONS = ["let"]
    VARIABLE_SEPARATOR = ","
    BOOLEAN_OPERATORS = ["and", "or", "not"]
    COMPARISON_OPERATORS = ["<", ">", ">=", "<=", "?=", "<>"]
    COMPARISON_CHARACTERS = "<>=?"
    KEYWORDS = ["print", "if", "elif", "else", "while"]
    SEPARATORS = "{}"

    def __init__(self, line: str, line_number: int) -> None:
        self.line = line
        self.index = 0
        self.tokens = []
        self.character = self.line[self.index]
        self.current_token = None
        self.brackets_count = 0
        self.line_number = line_number
        self.statement_type = None

    def forward(self) -> None:
        self.index += 1
        if self.index < len(self.line):
            self.character = self.line[self.index]

    def extract_word(self) -> str:
        word = ""
        while self.character in Lexer.VALID_VARIABLE_CHARACTERS and (self.index < len(self.line)):
            word += self.character
            self.forward()

        return word
    
    def extract_comparison_operator(self) -> str:
        comparison_operator = ""
        while self.character in Lexer.COMPARISON_CHARACTERS and self.index < len(self.line):
            comparison_operator += self.character
            self.forward()
        return comparison_operator
    
    def extract_number(self) -> str:
        number = ""
        is_float = False

        while (self.character in Lexer.NUMBERS or self.character == ".") and (self.index < len(self.line)):
            if self.character == "." and not is_float:
                is_float = True
            elif self.character == "." and is_float:
                return Error("Not a number.", self.index)
            
            number += self.character
            self.forward()

        return Integer(number) if not is_float else Float(number)

    def tokenize(self) -> tuple:
        while self.index < len(self.line):
            if self.character in Lexer.STOP_WORDS:
                self.forward()
                continue

            elif self.character in Lexer.OPERATORS:
                if self.character == "(":
                    self.brackets_count += 1
                elif self.character == ")":
                    self.brackets_count -= 1

                if self.character == "=":
                    self.statement_type = StatementType("assignment")

                self.current_token = Operator(self.character)
                self.forward()

            elif self.character in Lexer.NUMBERS:
                number = self.extract_number()
                if isinstance(number, Error):
                    return number
            
                self.current_token = number

            elif self.character in Lexer.LETTERS:
                word = self.extract_word()
                if word in Lexer.DECLARATIONS:
                    self.statement_type = StatementType("declaration")
                    self.current_token = Declaration(word)

                elif word in Lexer.BOOLEAN_OPERATORS:
                    self.current_token = BooleanOperator(word)

                elif word in Lexer.KEYWORDS:
                    self.statement_type = StatementType(word)
                    self.current_token = Keyword(word)

                else:
                    if self.index > 1 and self.tokens[0].value == word and self.statement_type.type == "assignment":
                        self.statement_type = StatementType("update")
                    self.current_token = Variable(word)

            elif self.character in Lexer.SEPARATORS:
                self.current_token = Separator(self.character)
                self.forward()

            elif self.character == Lexer.VARIABLE_SEPARATOR:
                self.current_token = VariableSeparator()
                self.forward()

            elif self.character in Lexer.COMPARISON_CHARACTERS:
                comparison_operator = self.extract_comparison_operator()
                self.current_token = ComparisonOperator(comparison_operator)

            elif self.character == ";":
                self.forward()
                continue

            else:
                return Error("Invalid syntax.", self.line_number, self.index)
            
            self.tokens.append(self.current_token)
        
        if self.brackets_count != 0:
            return Error("Invalid number of brackets", self.line_number, 0)

        return self.tokens, self.statement_type

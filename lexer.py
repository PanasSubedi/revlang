from tokens import Declaration, Variable, VariableSeparator,\
    StatementEnder, Operator, Integer, Float

from error import Error

class Lexer:

    NUMBERS = "0123456789"
    LETTERS = "abcdefghijklmnopqrstuvwxyz"
    VALID_VARIABLE_CHARACTERS = LETTERS + NUMBERS + "_"
    OPERATORS = "=+-*/()"
    STOP_WORDS = [" "]
    DECLARATIONS = ["let"]
    VARIABLE_SEPARATOR = ","
    STATEMENT_ENDER = ";"

    def __init__(self, line: str) -> None:
        self.line = line
        self.index = 0
        self.tokens = []
        self.character = self.line[self.index]
        self.current_token = None
        self.brackets_count = 0

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

    def tokenize(self) -> list:
        while self.index < len(self.line):
            if self.character in Lexer.STOP_WORDS:
                self.forward()
                continue

            elif self.character in Lexer.OPERATORS:
                if self.character == "(":
                    self.brackets_count += 1
                elif self.character == ")":
                    self.brackets_count -= 1
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
                    self.current_token = Declaration(word)

                else:
                    self.current_token = Variable(word)

            elif self.character == Lexer.VARIABLE_SEPARATOR:
                self.current_token = VariableSeparator()
                self.forward()

            elif self.character == Lexer.STATEMENT_ENDER:
                self.current_token = StatementEnder()
                self.forward()

            else:
                return Error("Invalid syntax.", self.index)

            self.tokens.append(self.current_token)

        if self.current_token.type != "END":
            return Error("Invalid statement end.", self.index)
        
        if self.brackets_count != 0:
            return Error("Invalid number of brackets.", 0)
        
        return self.tokens

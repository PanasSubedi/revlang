from tokens import Declaration, Variable, VariableSeparator,\
    StatementEnder

from error import Error

class Lexer:

    STOP_WORDS = [" "]
    LETTERS = "abcdefghijklmnopqrstuvwxyz"
    NUMBERS = "0123456789"
    VALID_VARIABLE_CHARACTERS = LETTERS + NUMBERS + "_"
    DECLARATIONS = ["let"]
    VARIABLE_SEPARATOR = ","
    STATEMENT_ENDER = ";"

    def __init__(self, line: str) -> None:
        self.line = line
        self.index = 0
        self.tokens = []
        self.character = self.line[self.index]
        self.current_token = None

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

    def tokenize(self) -> list:
        while self.index < len(self.line):
            if self.character in Lexer.STOP_WORDS:
                self.forward()
                continue

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
        
        return self.tokens

from lexer import Lexer
from error import Error
from parse import Parser
from interpreter import Interpreter
from data import Data

PROMPT = "$> "

base = Data()

while True:
    line = input(PROMPT)
    if line.lower() in ("x", "exit"):
        break

    lexer = Lexer(line)
    result = lexer.tokenize()

    if isinstance(result, Error):
        print(f"{' '*(result.index + len(PROMPT))}^\nError: {result.description}")
    else:
        tokens = lexer.tokenize()
        print(f"Tokens: {tokens}")

        parser = Parser(tokens)
        tree = parser.parse()

        print(f"Tree: {tree}")

        interpreter = Interpreter(tree, base)
        result = interpreter.interpret()

        print(f"Result: {result}")



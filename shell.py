from lexer import Lexer
from error import Error
from parse import Parser
from interpreter import Interpreter
from data import Data

PROMPT = "$> "

base = Data()

while True:

    statement_complete = False
    braces_count = 0
    all_tokens = []
    while not statement_complete:
        line = input(PROMPT)
        lexer = Lexer(line, braces_count)
        result = lexer.tokenize()

        if line == "x": break

        if isinstance(result, Error):
            print(f"{' '*(result.index + len(PROMPT))}^\nError: {result.description}")
        else:
            all_tokens.append(result[0])
            braces_count = result[1]
            statement_complete = braces_count == 0

    if len(all_tokens) == 0 and line == "x": break
    print(f"All tokens: {all_tokens}")

    all_trees = []
    for tokens in all_tokens:
        parser = Parser(tokens)
        tree = parser.parse()

        all_trees.append(tree)

    print(f"Trees: {all_trees}")

    results = []
    for tree in all_trees:
        interpreter = Interpreter(tree, base)
        result = interpreter.interpret()

        if result is not None:
            print(result.value)



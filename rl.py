import sys

from lexer import Lexer
from error import Error
from parse import Parser
from interpreter import Interpreter
from data import Data

def run_line(line, base):
    if line.lower() == "data":
        print(base.read_all())
        return True

    lexer = Lexer(line)
    tokens = lexer.tokenize()

    if isinstance(tokens, Error):
        print(f"{' '*(tokens.index)}^\nError: {tokens.description}")
        return False
    else:
        parser = Parser(tokens)
        tree = parser.parse()

        interpreter = Interpreter(tree, base)
        result = interpreter.interpret()

        print(result)
    
    return True


def run(code):

    base = Data()
    for line in code:
        line = line.strip()
        if len(line) != 0 and (not run_line(line, base)):
            break



def main(filename):
    with open(filename, "r") as file:
        code = file.readlines()

    run(code)


if __name__ == "__main__":

    args = sys.argv
    if len(args) == 2:
        main(args[1])
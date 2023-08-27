import sys

from lexer import Lexer
from error import Error
from parse import Parser
from interpreter import Interpreter
from data import Data

def run(code):
    pass

def main(filename):
    with open(filename, "r") as file:
        code = file.readlines()
    run(code)


if __name__ == "__main__":
    args = sys.argv
    if len(args) == 2:
        main(args[1])
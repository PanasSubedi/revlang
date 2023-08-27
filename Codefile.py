from lexer import Lexer
from parse import Parser
from interpreter import Interpreter
from data import Data
from error import Error

from tokens import BoolResult

class Code:
    def __init__(self, filename=None, data=None, verbose=False, stepping=False) -> None:
        self.filename = filename
        self.code = None
        self.data = Data() if data is None else data
        self.current_line = ""
        self.index = -1
        self.verbose = verbose
        self.stepping = stepping

    def back_to_start(self) -> None:
        self.index = self.block["block_start"]
        self.back()

    def back(self) -> None:
        prev_line_found = False
        while not prev_line_found:
            self.index -= 1
            if self.index > -1:
                self.current_line = self.code[self.index]
                if len(self.current_line.strip()) > 0:
                    prev_line_found = True
            else:
                prev_line_found = True

    def forward(self) -> None:
        next_line_found = False
        while not next_line_found:
            self.index += 1
            if self.index < len(self.code):
                self.current_line = self.code[self.index]
                if len(self.current_line.strip()) > 0:
                    next_line_found = True
            else:
                next_line_found = True

    def set_code(self, code):
        self.code = code

    def load(self) -> None:
        with open(self.filename, "r") as file:
            self.code = file.readlines()

    def get_line(self) -> str:
        line = self.current_line.strip()
        return line
    
    def interpret_line(self, line, direction):
            if line.startswith("if"):
                result = self.interpret_if_block()
                if isinstance(result, Error):
                    Error.display_error(result)
            elif line.startswith("while"):
                return self.interpret_while_block()
            elif line[-1] == ";":
                self.run_line(direction)
            elif line[-1] == "}" and direction == 0:
                self.interpret_block_reverse()
            elif line[-1] == "}":
                return
            else:
                error = Error("Missing semi-colon", self.index+1, len(line))
                Error.display_error(error)
                return
            
    def interpret_block_reverse(self):
        start_found = False
        end_index = self.index
        index = self.index
        found_block = ""

        while index > -1 and not start_found:
            line = self.code[index]

            if line.startswith("while"):
                start_found = True
                start_index = index
                found_block = "while"
            elif line.startswith("if"):
                start_found = True
                start_index = index
                found_block = "if"
            else:
                index -= 1

        if found_block == "while":
            self.interpret_while_block_reverse(start_index, end_index)
        elif found_block == "if":
            self.interpret_if_block_reverse(start_index)

    def interpret_while_block_reverse(self, start_index, end_index):
        while_meta = self.data.read_meta(start_index)
        count = while_meta.get("count")

        while True:
            line = self.get_line()

            if count == 0:
                self.index = start_index
                break

            elif line == "}":
                self.back()

            elif line.startswith("while"):
                count -= 1
                self.index = end_index
                self.back()

            else:
                line = self.get_line()
                self.interpret_line(line, 0)
                self.back()

    def interpret_while_block(self) -> None:
        start_index = self.index
        end_index = None
        count = 0
        self.data.store_meta(start_index, {
            "end": end_index,
            "count": count
        })

        while True:
            line = self.get_line()

            if line == "}":
                count += 1
                end_index = self.index

                self.data.store_meta(start_index, {
                    "end": end_index,
                    "count": count,
                })

                self.index = start_index-1
                self.forward()

            else:
                result = self.run_line()
                if isinstance(result, BoolResult) and result.value.value:
                    while True:
                        self.forward()
                        line = self.get_line()
                        result = self.interpret_line(line, 1)
                        
                        if isinstance(result, Error): break
                        if line.startswith("}"): break
                else:
                    while True:
                        self.forward()
                        line = self.get_line()
                        if line.startswith("}"):
                            return

    def interpret_if_block_reverse(self, start_index) -> None:
        if_meta = self.data.read_meta(start_index)
        entered_block = if_meta.get("entered_block")
        total_blocks = if_meta.get("total_blocks")

        current_block = total_blocks
        entered_a_block = False

        while True:
            line = self.get_line()

            if entered_block is None or entered_a_block:
                self.index = start_index
                break

            elif current_block == entered_block:
                entered_a_block = True
                while True:
                    self.back()
                    line = self.get_line()
                    if line.startswith("}") or line.startswith("if"):
                        break
                    self.interpret_line(line, 0)
            else:
                while True:
                    self.back()
                    line = self.get_line()
                    if line.startswith("}"):
                        break
                current_block -= 1

    def interpret_if_block(self) -> None:
        start_index = self.index
        entered_a_block = False
        entered_block = None
        block_number = 0
        total_blocks = 0

        while True:
            line = self.get_line()

            if line == "}":
                end_index = self.index
                self.data.store_meta(start_index, {
                    "end": end_index,
                    "entered_block": entered_block,
                    "total_blocks": total_blocks,
                })
                return
            elif entered_a_block:
                while line != "}":
                    self.forward()
                    if line.startswith("}"):
                        total_blocks += 1
                    line = self.get_line()
            else:
                block_number += 1
                result = self.run_line()
                if isinstance(result, BoolResult) and result.value.value:
                    entered_block = block_number
                    entered_a_block = True
                    while True:
                        self.forward()
                        line = self.get_line()
                        if line.startswith("}"):
                            total_blocks += 1
                            break

                        self.interpret_line(line, 1)
                else:
                    while True:
                        self.forward()
                        line = self.get_line()
                        if line.startswith("}"):
                            total_blocks += 1
                            break

    def run(self) -> None:

        if self.code is not None:
            
            current_direction = 1
            while self.index < len(self.code)-1:

                if self.stepping:
                    direction = input("Direction? ")
                    current_direction = 0 if direction == "r" else 1

                if current_direction == 1:
                    self.forward()
                    line = self.get_line()
                    result = self.interpret_line(line, current_direction)
                    if isinstance(result, Error):
                        break

                elif self.index > -1:
                    line = self.get_line()
                    result = self.interpret_line(line, current_direction)
                    if isinstance(result, Error):
                        break
                    self.back()

                else:
                    print("Unable to go back.")

    def check_error(self, result) -> None:
        if isinstance(result, Error):
            Error.display_error(result)
            return True
        return False

    def run_line(self, direction=1) -> None:
        line = self.get_line()
        line_number = self.index + 1

        lexer = Lexer(line, line_number)
        tokens, statement_type = lexer.tokenize()

        if not self.check_error(tokens):
            if self.verbose: print(tokens)

            parser = Parser(tokens, direction=direction, statement_type=statement_type)
            tree = parser.parse()

            if not self.check_error(tree):
                if self.verbose: print(tree)


                interpreter = Interpreter(tree, self.data, direction, line_number, statement_type)
                result = interpreter.interpret()

                if not self.check_error(result):
                    if self.verbose: print(result)

                    if not isinstance(result, BoolResult):
                        if statement_type.type == "print":
                            print(result.value)
                        elif statement_type.type == "assignment":
                            self.data.store_meta(self.index, {
                                "original": result
                            })
                        elif statement_type.type in ("declaration", "update"):
                            pass
                        else:
                            if result is not None:
                                print(result.value)
                    else:
                        return result

                    if self.stepping:
                        print(self.data.read_all())
                        print("\n")
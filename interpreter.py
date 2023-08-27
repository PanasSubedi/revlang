from tokens import Float, Integer, BoolResult

class Interpreter:
    def __init__(self, tree, base, direction=1, line_number=None, statement_type=None) -> None:
        self.tree = tree
        self.data = base
        self.direction = direction
        self.line_number = line_number
        self.statement_type = statement_type

    def convert_INT(self, value): return int(value)
    def convert_FLT(self, value): return float(value)
    def convert_VAR(self, id):
        data = self.data.read(id)
        return None if data is None else getattr(self, f"convert_{data.type}")(data.value)

    def compute_single(self, operand):
        operand_type = "VAR" if str(operand.type).startswith("VAR") else str(operand.type)
        output = getattr(self, f"convert_{operand_type}")(operand.value)

        if operand_type == "VAR":
            output_check = self.data.read(operand.value)
            if output_check is None:
                return None
            else:
                output_check = output_check.type
        else:
            output_check = operand.type

        return Integer(output) if output_check == "INT" else Float(output)

    def compute_unary(self, operator, operand) -> None:
        operand_type = "VAR" if str(operand.type).startswith("VAR") else str(operand.type)
        operand = getattr(self, f"convert_{operand_type}")(operand.value)

        if operator.value == "+": output = operand
        elif operator.value == "-": output = -operand
        elif operator.value == "not": output = 1 if not operand else 0

        return Integer(output) if operand_type == "INT" else Float(output)

    def compute_binary(self, left, operator, right):
        left_type = "VAR" if str(left.type).startswith("VAR") else str(left.type)
        right_type = "VAR" if str(right.type).startswith("VAR") else str(right.type)

        if operator.value == "=":

            if self.direction == 0 and self.statement_type.type == "assignment":
                original_token = self.data.meta.get(int(self.line_number)-1).get("original", None)
                if original_token is None:
                    left.type = f"VAR(?)"
                    self.data.write(left, None)
                else:
                    left.type = f"VAR({original_token.type})"
                    self.data.write(left, original_token)
                return
                
            else:
                left.type = f"VAR({right_type})"
                original_value = self.data.read(left.value)
                self.data.write(left, right)
                return original_value
        
        left = getattr(self, f"convert_{left_type}")(left.value)
        right = getattr(self, f"convert_{right_type}")(right.value)

        if operator.value == "+": output = left + right
        elif operator.value == "-": output = left - right
        elif operator.value == "*": output = left * right
        elif operator.value == "/": output = left / right
        elif operator.value == "and": output = 1 if left and right else 0
        elif operator.value == "or": output = 1 if left or right else 0
        elif operator.value == "<": output = 1 if left < right else 0
        elif operator.value == ">": output = 1 if left > right else 0
        elif operator.value == "<=": output = 1 if left <= right else 0
        elif operator.value == ">=": output = 1 if left >= right else 0
        elif operator.value == "?=": output = 1 if left == right else 0
        elif operator.value == "<>": output = 1 if left != right else 0

        return Float(output) if (isinstance(left, float) or isinstance(right, float) or operator.value == "/") else Integer(output)

    def interpret(self, tree=None):
        if tree is None: tree = self.tree

        if isinstance(tree, list) and len(tree) == 2:
            if tree[0].type == "DECL":
                variables = tree[1]
                for variable in variables:
                    if self.direction == 1:
                        self.data.write(variable, None)
                    else:
                        self.data.remove(variable)
                return
            elif tree[0].value == "print":
                return self.interpret(tree[1])
            elif tree[0].value in ("if", "elif"):
                return BoolResult(self.interpret(tree[1]))
            elif tree[0].value in ("else"):
                return BoolResult(Integer(1))
            elif tree[0].value == "while":
                return BoolResult(self.interpret(tree[1]))
            else:
                expression = tree[1]
                if isinstance(expression, list):
                    expression = self.interpret(expression)
                return self.compute_unary(tree[0], expression)
            
        elif not isinstance(tree, list):
            return tree
        
        elif len(tree) == 1:
            return self.compute_single(tree[0])
        
        else:
            left_node = tree[0]
            if isinstance(left_node, list):
                left_node = self.interpret(left_node)
            right_node = tree[2]
            if isinstance(right_node, list):
                right_node = self.interpret(right_node)
            operator = tree[1]

            return self.compute_binary(left_node, operator, right_node)

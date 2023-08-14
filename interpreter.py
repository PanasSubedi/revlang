from tokens import Float, Integer

class Interpreter:
    def __init__(self, tree, base) -> None:
        self.tree = tree
        self.data = base

    def convert_INT(self, value): return int(value)
    def convert_FLT(self, value): return float(value)
    def convert_VAR(self, id): return getattr(self, f"convert_{self.data.read(id).type}")(self.data.read(id).value)

    def compute_binary(self, left, operator, right) -> None:
        left_type = "VAR" if str(left.type).startswith("VAR") else str(left.type)
        right_type = "VAR" if str(right.type).startswith("VAR") else str(right.type)

        if operator.value == "=":
            left.type = f"VAR({right_type})"
            self.data.write(left, right)
            return self.data.read_all()
        
        left = getattr(self, f"convert_{left_type}")(left.value)
        right = getattr(self, f"convert_{right_type}")(right.value)

        if operator.value == "+": output = left + right
        elif operator.value == "-": output = left - right
        if operator.value == "*": output = left * right
        if operator.value == "/": output = left / right

        return Float(output) if ("FLT" in (left_type, right_type) or operator.value == "/") else Integer(output)

    def interpret(self, tree=None):
        if tree is None: tree = self.tree

        if isinstance(tree, list) and len(tree) == 2:
            if tree[0].type == "DECL":
                variables = tree[1]
                for variable in variables:
                    self.data.write(variable, None)
                return self.data.read_all()
            
        elif not isinstance(tree, list):
            return tree
        
        else:
            left_node = tree[0]
            if isinstance(left_node, list):
                left_node = self.interpret(left_node)
            right_node = tree[2]
            if isinstance(right_node, list):
                right_node = self.interpret(right_node)
            operator = tree[1]

            return self.compute_binary(left_node, operator, right_node)

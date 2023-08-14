class Interpreter:
    def __init__(self, tree, base) -> None:
        self.tree = tree
        self.data = base

    def compute_binary(self, left, operator, right) -> None:
        #left_type = "VAR" if str(left.type).startswith("VAR") else str(left.type)
        right_type = "VAR" if str(right.type).startswith("VAR") else str(right.type)

        if operator.value == "=":
            left.type = f"VAR({right_type})"
            self.data.write(left, right)
            return self.data.read_all()

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
            right_node = tree[2]
            operator = tree[1]

            return self.compute_binary(left_node, operator, right_node)

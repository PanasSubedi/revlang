class Interpreter:
    def __init__(self, tree, base) -> None:
        self.tree = tree
        self.data = base

    def interpret(self, tree=None):
        if tree is None: tree = self.tree

        if isinstance(tree, list) and len(tree) == 2:
            if tree[0].type == "DECL":
                variables = tree[1]
                for variable in variables:
                    self.data.write(variable, None)
                return self.data.read_all()

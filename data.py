class Data:
    def __init__(self) -> None:
        self.variables = {}
        self.meta = {}

    def increase_if_count(self):
        self.meta["if_count"] = self.meta.get("if_count", 0) + 1

    def read(self, id):
        return self.variables.get(id)
    
    def read_all(self):
        return self.variables
    
    def remove(self, variable):
        variable_name = variable.value
        del self.variables[variable_name]
    
    def write(self, variable, expression):
        variable_name = variable.value
        self.variables[variable_name] = expression

    def store_meta(self, line_number, object):
        self.meta[line_number] = object

    def read_meta(self, line_number) -> dict:
        return self.meta[line_number]
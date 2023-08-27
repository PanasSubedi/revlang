class Error:
    def __init__(self, description, line_number, index) -> None:
        self.description = description
        self.index = index
        self.line_number = line_number

    @staticmethod
    def display_error(error) -> None:
        print(f"Line {error.line_number}:{error.index} {error.description}")
class ColumnFullError(Exception):
    def __init__(self, message):
        super().__init__(message)

class UsernameError(Exception):
    def __init__(self, message):
        super().__init__(message)

class ColorError(Exception):
    def __init__(self, message):
        super().__init__(message)

class PieceTypeError(Exception):
    def __init__(self, message):
        super().__init__(message)
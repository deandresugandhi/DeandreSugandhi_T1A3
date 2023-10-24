"""
Module for custom errors.
"""

class ColumnFullError(Exception):
    """
    Error raised when a player attempt to drop a piece on a game board column
    that is already full.
    """
    def __init__(self, message):
        super().__init__(message)

class UsernameError(Exception):
    """Error raised when username or player name does not match format."""
    def __init__(self, message):
        super().__init__(message)

class ColorError(Exception):
    """Error raised when a color value is not a valid color for termcolor."""
    def __init__(self, message):
        super().__init__(message)

class PieceTypeError(Exception):
    """Error raised when piece type does not match format."""
    def __init__(self, message):
        super().__init__(message)
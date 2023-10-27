"""
A module containing classes that represents the objects involved to play 
Connect Four, namely the game board and game pieces.
"""


# Standard Library Modules
import re

# Third-party Library Modules
from termcolor import colored
import art
import numpy as np

# Local Modules
from custom_errors import (
    ColumnFullError,
    UsernameError,
    ColorError,
    PieceTypeError
)


class Piece:
    """
    Represents a game piece used in the game.
    
    The game piece is a visualization of a player's piece on the board. The
    appearance can be customized by changing a Piece instance's attributes.

    Attributes:
    1. _player_name (str): The name of the player owning the piece.
    2. _color (str): The color of the piece.
    3. _piece_type (str): The visual representation of the piece
       (i.e. its shape)
    4. _player (Player): The player number of the piece (i.e. p1 or p2)
    5. surrender (bool): Represents whether the owner of the piece surrendered.
    """
    def __init__(self, player_name, color, piece_type, player):
        self._player_name = player_name
        self._color = color
        self._piece_type = piece_type
        self._player = player
        self.surrender = False

    @property
    def player_name(self):
        """A method to access the player's name."""
        return self._player_name

    @player_name.setter
    def player_name(self, player_name):
        """
        A method to set the player's name. It includes validation to make sure
        it is in the right format (alphanumeric, periods, and underscores only,
        5-20 characters long, name must start and end with an alphanumeric 
        character). 
        
        Raises custom UsernameError if format is not followed.  
        """
        if re.fullmatch("^[a-zA-Z0-9][a-zA-Z0-9._-]{3,18}[a-zA-Z0-9]$",
            player_name):
            self._player_name = player_name
        else:
            raise UsernameError("Invalid player name.")

    @property
    def color(self):
        """A method to access the piece color."""
        return self._color.lower()

    @color.setter
    def color(self, color):
        """
        A method to set the piece color. Termcolor module's colored() function
        is used to test the value assigned as the _color attribute. Termcolor
        will raise KeyError if it fails to color the string using the value.

        Raises ColorError if KeyError is raised by termcolor module. If no error
        is raised, the _color attribute is set to the value of color in lower
        case for consistency.
        """
        try:
            colored("test", color)
        except KeyError as exc:
            raise ColorError("Invalid color.") from exc
        self._color = color.lower()

    @property
    def piece_type(self):
        """A method to access the piece type."""
        return self._piece_type

    @piece_type.setter
    def piece_type(self, piece_type):
        """
        A method to set the piece type. It includes validation to make sure
        it is in the right format (alphanumeric and 1 character long). 
        
        Raises custom PieceTypeError if format is not followed.
        """
        if re.fullmatch("^[a-zA-Z0-9]$", piece_type):
            self._piece_type = piece_type
        else:
            raise PieceTypeError("Invalid piece type. Please try again.")

    @property
    def player(self):
        """A method to access the piece's player number."""
        return self._player

    @property
    def surrender(self):
        """A method to access the piece's player's surrender state."""
        return self._surrender

    @surrender.setter
    def surrender(self, surrender):
        """A method to set the piece's players's surrender state."""
        self._surrender = surrender

    def drop(self, board, column):
        """
        A method to drop the piece onto the board. Players 1's piece would be
        represented as a "1" in the board's array, and players 2's piece would
        be represented as a "2" in the board's array.

        Args:
        1. board (Board): An instance of the Board class, defining the board 
           onto which the piece will be dropped.
        2. column (str): A string digit representing the column number of the
           board to drop the piece onto
        """
        row = -1
        while board.array[row, column - 1] != "0":
            row -= 1
            if row < -6:
                raise ColumnFullError("Column is full. Please try again: ")
        board.array[row, column - 1] = self.player


class Board:
    """
    Represents a game board used in the game.
    
    The game board is a 6 x 7 Connect Four board. It functions as a NumPy array
    which is translated and displayed on the terminal through various methods.

    Attributes:
    1. _array (np.array): A NumPy array with 6 lists (representing rows) with
       7 elements each (representing columns). 0 represents an empty space
       in the cage.
    2. _edge (str): Component used to display the board. It is the bottom edge 
       of the game board, representing the slider to clear the board.
    3. _divider (str): Component used to display the board. Represents the 
       dividers between each row of the game board.
    4. _column (list): A list of components to display the board. Represents
       each "cage" of the board, i.e. the columns.
    5. players (list): A list of Piece class instances, defining the pieces and
       players that is playing on the board, accessing its properties such as
       piece color, piece type, player name, etc to be displayed by the board.
    """
    def __init__(self, players):
        self._array = np.array([["0" for i in range(7)] for i in range(6)])
        self._edge = "+===" *7 + "+"
        self._divider = "+---"*7 + "+"
        self._column = [f"  {i+1} " for i in range(7)]
        self._players = players

    @property
    def players(self):
        """A method to access the board's players, a list of Piece instances."""
        return self._players

    @players.setter
    def players(self, players):
        """A method to set the board's players, a list of Piece instances."""
        self._players = players

    @property
    def array(self):
        """A method to access the board's array."""
        return self._array

    @array.setter
    def array(self, array):
        """A method to set the board's array."""
        self._array = array

    def display(self):
        """A method to display the board array's visual representation."""
        # Create a dictionary as a reference to display the board. "1" key
        # refers to players 1's piece representation in the board (from the
        # Piece.drop() method), "2" key refers that of player 2's. Value is
        # the Piece instance's _piece_type colored with its _color.
        piece_dict = {
            "0": " ",
            "1": colored(self.players[0].piece_type, self.players[0].color),
            "2": colored(self.players[1].piece_type, self.players[1].color),
        }

        # Creates a CONNECT 4 ASCII art logo
        logo = colored(
               art.text2art("CONNECT 4", font="small", space = 0),
               "light_grey")

        # Prints the visual representation of the array on the board.
        # Prints CONNECT 4 logo sliced to remove its built-in line breaks
        print(logo[0:-10])
        # Prints player names and preview of their pieces' representation
        # centered to the board.
        print(
            f"{self._players[0].player_name} = {piece_dict.get('1')}".center(58)
            )
        print(
            f"{self._players[1].player_name} = {piece_dict.get('2')}".center(58)
            )
        # Prints the heading "COLUMN NUMBER" centered to the board.
        print(colored("\n" + "        COLUMN NUMBER        ".center(50), "white"))
        # Prints the column numbers above each column, centered to the board.
        print(
            "          " + colored("".join(self._column) + " ",
            "black", "on_white")
            )

        # Prints the actual game board.
        cage_row = ""
        for row in self._array:
            print(self._divider.center(50))
            # Displays the content of each slot in the board based on the dict.
            for slot in row:
                # Adds each slot into cage_row, to form display of a row
                cage_row += f"| {piece_dict.get(slot)} "
            # Prints the row, with space in the beginning to center the board.
            print(" " * 10 + cage_row + "|")
            cage_row = ""
        # Prints the slider of the board
        print(self._edge.center(50))

    def clear_board(self):
        """A method to clear the board, equivalent to pulling board slider"""
        self.array = np.array([["0" for i in range(7)] for i in range(6)])

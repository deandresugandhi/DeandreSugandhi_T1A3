"""
Module that contains the VictoryChecker class, representing the game's referee.
Defines the win logic of the game.
"""

class VictoryChecker:
    """
    An instance of this class represents the referee of the game.
    
    The referee checks whether a player has won or surrendered based on the 
    current state of the game board and Piece instances. The class's methods
    defines the win conditions of the game.

    Attributes:
    1. _board (Board): The Board instance where the game is played.
    2. _piece1 (Piece): The Piece instance representing player 1.
    3. _piece2 (Piece): The Piece instance representing player 2.
    """
    def __init__(self, board, players):
        self._board = board
        self._piece1 = players[0]
        self._piece2 = players[1]

    def horizontal_victory(self):
        """
        Defines how the referee detects 4 game pieces aligned horizontally.
        
        Returns the Piece instance that won based on this condition, or None
        if no Piece instances satisfied the condition.
        """
        for row in self._board.array:
            for i in range(4):
                if all(slot == "1" for slot in row[i:i + 4]):
                    return self._piece1
                if all(slot == "2" for slot in row[i:i + 4]):
                    return self._piece2
        return None

    def vertical_victory(self):
        """
        Defines how the referee detects 4 game pieces aligned vertically.
        
        Returns the Piece instance that won based on this condition, or None
        if no Piece instances satisfied the condition.
        """
        for i_row in range(3):
            for i_column in range(7):
                if all(self._board.array[i_row:i_row + 4, i_column] == "1"):
                    return self._piece1
                if all(self._board.array[i_row:i_row + 4, i_column] == "2"):
                    return self._piece2
        return None

    def diagonal_victory(self):
        """
        Defines how the referee detects 4 game pieces aligned diagonally.
        
        Returns the Piece instance that won based on this condition, or None
        if no Piece instances satisfied the condition.
        """
        for i_row in range(3):
            for i_column in range(4):
                # if (north-west to south-east diagonal or
                #     south-west to north-east diagonal)
                if (all(self._board.array[i + i_row, i + i_column] == "1" for i in range(4)) or
                    all(self._board.array[i + i_row, (3 + i_column) - i] == "1" for i in range(4))
                ):
                    return self._piece1
                if (all(self._board.array[i + i_row, i + i_column] == "2" for i in range(4)) or
                    all(self._board.array[i + i_row, (3 + i_column) - i] == "2" for i in range(4))
                ):
                    return self._piece2
        return None

    def surrender(self):
        """
        Defines how surrenders are implemented. Reads the surrender attribute
        from the Piece instances.
        
        Returns the Piece instance that that did not surrender if one of the 
        Piece instances has their surrender attribute set to True, or None if 
        none has their surrender attribute set to True.
        """
        if self._piece1.surrender:
            return self._piece2
        if self._piece2.surrender:
            return self._piece1
        return None

    def check_victory(self):
        """
        Combines all the methods to check if any piece satisfies at least one
        of the three winning conditions.

        Returns the Piece instance that satisfies at least one winning
        condition, or None if none is detected.
        """
        winner = (
            self.horizontal_victory() or
            self.vertical_victory() or
            self.diagonal_victory() or
            self.surrender()
        )

        if winner is not None:
            return winner
        return None

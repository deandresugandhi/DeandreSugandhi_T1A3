class VictoryChecker:
    def __init__(self, board, piece1, piece2):
        self._board = board
        self._piece1 = piece1
        self._piece2 = piece2

    def horizontal_victory(self):
        for row in self._board.array:
            for i in range(4):
                if all(slot == 1 for slot in row[i:i + 4]):
                    return self._piece1._player_name
                elif all(slot == 2 for slot in row[i:i + 4]):
                    return self._piece2._player_name
        return None

    def vertical_victory(self):
        for i_row in range(3): 
            for i_column in range(7):
                if all(self._board.array[i_row:i_row + 4, i_column] == 1):
                    return self._piece1._player_name
                elif all(self._board.array[i_row:i_row + 4, i_column] == 2):
                    return self._piece2._player_name
        return None

    def diagonal_victory(self):
        for i_row in range(3):
            for i_column in range(4):
                if all(self._board.array[i + i_row, i + i_column] == 1 for i in range(4)) or all(self._board.array[i + i_row, (3 + i_column) - i] == 1 for i in range(4)):
                    return self._piece1._player_name
                elif all(self._board.array[i + i_row, i + i_column] == 2 for i in range(4)) or all(self._board.array[i + i_row, (3 + i_column) - i] == 2 for i in range(4)):
                    return self._piece2._player_name
        return None
    
    def surrender(self):
        if self._piece1.surrender:
            return self._piece2._player_name
        elif self._piece2.surrender:
            return self._piece1._player_name
        return None

    def check_victory(self):
        winner = self.horizontal_victory() or self.vertical_victory() or self.diagonal_victory() or self.surrender()
        if winner is not None:
            return winner
        return None
    



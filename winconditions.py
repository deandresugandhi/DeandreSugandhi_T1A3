def horizontal_victory(board, piece1, piece2):
    for row in board._array:
        for i in range(4):
            if all(row[i:i+4]):
                return f"{piece1._player_name} wins"
            elif all(slot > 1 for slot in row[i:i + 4]):
                return f"{piece2._player_name} wins"
            else:
                continue

def vertical_victory(board, piece1, piece2):
    for i_column in range(7): 
        for i_row in range(3):
            if all(board._array[i_row:i_row + 4, i_column]):
                return f"{piece1._player_name} wins"
            elif all(slot > 1 for slot in board._array[i_row:i_row + 4, i_column]):
                return f"{piece2._player_name} wins"
            else:
                continue

def diagonal_victory(board, piece1, piece2):
    for i_row in range(3):
        # North-West to South-East diagonal
        for i_column in range(4):
            if all(board._array[i + i_row, i + i_column] for i in range(4)):
                return f"{piece1._player_name} wins"
            elif all(slot > 1 for slot in (board._array[i + i_row, i + i_column] for i in range(4))):
                return f"{piece2._player_name} wins"
            else:
                continue
        # South-West to North-East diagonal
        for i_column in range(4):
            if all(board._array[i + i_row, (3 + i_column) - i] for i in range(4)):
                return f"{piece1._player_name} wins"
            if all(slot > 1 for slot in (board._array[i + i_row, (3 + i_column) - i] for i in range(4))):
                return f"{piece2._player_name} wins"
            else:
                continue


# iter0 = 10 21 32 43
# iter1 = 01 12 23 34
# iter2 = 02 13 24 35


# iter0 = 03 12 21 30 / 30 21 12 03
# iter1 = 04 13 22 31 / 31 22 13 04
# iter2 = 05 14 23 32 / 32 23 14 05
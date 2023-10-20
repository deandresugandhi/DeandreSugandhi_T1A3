import numpy as np
from colorama import Fore
import colorama


colorama.init(autoreset=True)

class Board:
    def __init__(self):
        self._array = np.array([[0 for i in range(7)] for i in range(6)])
        self._edge = "+===" *7 + "+"
        self._divider = "+---"*7 + "+"
        self._column = [f"  {i+1} " for i in range(7)]

    def display(self):
        print(f"{Fore.RED}        COLUMN NUMBER        ")
        print(*self._column, sep="")
        for row in self._array:
            print(self._divider)
            for index, slot in enumerate(row):
                if index < 6:
                    print(f"| {slot} ".replace("0", " "), end="")
                else: 
                    print(f"| {slot} |".replace("0", " "))
        print(self._edge)

    def clear_board(self):
        self._array = np.array([[0 for i in range(7)] for i in range(6)])

class Piece:
    def __init__(self, player_name, color, piece_type, player):
        self._player_name = player_name
        self._color = color
        self._piece_type = piece_type
        self._player = player
    
    def drop(self, board, column):
        row = -1
        while board._array[row, column - 1] != 0:
            row -= 1
            if row < -6:
                print("No more space to drop!")
                return "Illegal move"
        board._array[row, column - 1] = self._player






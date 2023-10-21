import numpy as np
from colorama import Fore
import colorama
from termcolor import colored


colorama.init(autoreset=True)

class Piece:
    def __init__(self, player_name, color, piece_type, player):
        self._player_name = player_name
        self._color = color
        self._piece_type = piece_type
        self._player = player
    
    @property
    def color(self):
        return self._color.lower()
    
    @color.setter
    def color(self, color):
        self._color = color
    
    @property
    def piece_type(self):
        return self._piece_type
    
    @piece_type.setter
    def piece_type(self, piece_type):
        self._piece_type = piece_type

    def drop(self, board, column):
        row = -1
        while board._array[row, column - 1] != 0:
            row -= 1
            if row < -6:
                print("No more space to drop!")
                return "Illegal move"
        board._array[row, column - 1] = self._player


class Board:
    def __init__(self, players):
        self._array = np.array([[0 for i in range(7)] for i in range(6)])
        self._edge = "+===" *7 + "+"
        self._divider = "+---"*7 + "+"
        self._column = [f"  {i+1} " for i in range(7)]
        self._players = players

    def display(self):
        piece_dict = {
            0: " ",
            1: colored(players[0].piece_type, players[0].color),
            2: colored(players[1].piece_type, players[1].color),
        }
        print(f"{Fore.RED}        COLUMN NUMBER        ")
        print(*self._column, sep="")
        for row in self._array:
            print(self._divider)
            for index, slot in enumerate(row):
                if index < 6:
                    print(f"| {piece_dict.get(slot)} ", end="")
                else: 
                    print(f"| {piece_dict.get(slot)} |")
        print(self._edge)

    def clear_board(self):
        self._array = np.array([[0 for i in range(7)] for i in range(6)])
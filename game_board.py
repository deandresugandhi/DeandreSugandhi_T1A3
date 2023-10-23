import numpy as np
import colorama
from termcolor import colored
import re


colorama.init(autoreset=True)

class Piece:
    def __init__(self, player_name, color, piece_type, player):
        self._player_name = player_name
        self._color = color
        self._piece_type = piece_type
        self._player = player
        self.surrender = False
    
    @property
    def player_name(self):
        return self._player_name
    
    @player_name.setter
    def player_name(self, player_name): 
        if re.fullmatch("^[a-zA-Z0-9][a-zA-Z0-9._-]{3,18}[a-zA-Z0-9]$", player_name):
            self._player_name = player_name
        else:
            raise ValueError("Invalid name.")
        
    @property
    def color(self):
        return self._color.lower()
    
    @color.setter
    def color(self, color):
        try:
            colored("test", color)
        except KeyError:
            raise ValueError("Invalid color.")
        else:
            self._color = color.lower()
    
    @property
    def piece_type(self):
        return self._piece_type
    
    @piece_type.setter
    def piece_type(self, piece_type):
        if re.fullmatch("^[a-zA-Z0-9]$", piece_type):
            self._piece_type = piece_type
        else:
            raise ValueError("Invalid piece type. Please try again.")

    @property
    def player(self):
        return self._player

    @property
    def surrender(self):
        return self._surrender
    
    @surrender.setter
    def surrender(self, surrender):
        self._surrender = surrender

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

    @property
    def array(self):
        return self._array

    def display(self):
        piece_dict = {
            0: " ",
            1: colored(self._players[0].piece_type, self._players[0].color),
            2: colored(self._players[1].piece_type, self._players[1].color),
        }
        print(colored("\n" + "        COLUMN NUMBER        ", "white"))
        print(colored("".join(self._column) + " ", "black", "on_white"))
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
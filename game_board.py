import numpy as np
from termcolor import colored
import re
import art
from custom_errors import ColumnFullError

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
        while board._array[row, column - 1] != "0":
            row -= 1
            if row < -6:
                raise ColumnFullError("Column is full. Please try again: ")
        board._array[row, column - 1] = self._player


class Board:
    def __init__(self, players):
        self._array = np.array([["0" for i in range(7)] for i in range(6)])
        self._edge = "+===" *7 + "+"
        self._divider = "+---"*7 + "+"
        self._column = [f"  {i+1} " for i in range(7)]
        self._players = players

    @property
    def array(self):
        return self._array

    def display(self):
        piece_dict = {
            "0": " ",
            "1": colored(self._players[0].piece_type, self._players[0].color),
            "2": colored(self._players[1].piece_type, self._players[1].color),
        }
        logo = colored(art.text2art(f"CONNECT 4", font="small", space = 0), "light_grey")
        print(logo[0:-10])
        print(f"{self._players[0].player_name} = {piece_dict.get('1')}".center(58))
        print(f"{self._players[1].player_name} = {piece_dict.get('2')}".center(58))
        print(colored("\n" + "        COLUMN NUMBER        ".center(50), "white"))
        print("          "+ colored("".join(self._column)+ " ", "black", "on_white"))

        cage_row = ""
        for row in self._array:
            print(self._divider.center(50))
            for slot in row:
                cage_row += f"| {piece_dict.get(slot)} " 
            print(" " * 10 + cage_row + "|")
            cage_row = ""
        
        print(self._edge.center(50))

    def clear_board(self):
        self._array = np.array([["0" for i in range(7)] for i in range(6)])
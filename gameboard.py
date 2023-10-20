import numpy as np
from colorama import Fore
import colorama

colorama.init(autoreset=True)

edge = "+===" *7 + "+"
divider = "+---"*7 + "+"
column = [f"  {i+1} " for i in range(7)]

gameboard = np.array([[0 for i in range(7)] for i in range(6)])

def display_board():
    print(f"{Fore.RED}        COLUMN NUMBER        ")
    print(*column, sep="")
    for row in gameboard:
        print(divider)
        for index, slot in enumerate(row):
            if index < 6:
                print(f"| {slot} ".replace("0", " "), end="")
            else: 
                print(f"| {slot} |".replace("0", " "))
    print(edge)

class Piece:
    def __init__(self, color, piece_type, player):
        self.color = color
        self.piece_type = piece_type
        self.player = player
    def drop(self):
        gameboard[-1, 1] = self.player

player1 = Piece("red", "O", "1")
player2 = Piece("blue", "X", "2")

player2.drop()

display_board()


import numpy as np

edge = "+===" *7 + "+"
cage = "|   " * 7 + "|"
divider = "+---"*7 + "+"
column =[f"  {i+1} " for i in range(7)]

def display_board():
    print("        COLUMN NUMBER        ")
    print(*column, sep="")
    for i in range(6):
        print(divider)
        print(cage)
    print(edge)

display_board()

gameboard = np.array([[0 for i in range(7)] for i in range(6)])

print(gameboard)
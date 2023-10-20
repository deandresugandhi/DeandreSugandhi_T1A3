from gameboard import Board, Piece
import subprocess

def clear_screen():
    try:
        subprocess.run("cls", shell=True, check=True)
    except subprocess.CalledProcessError:
        subprocess.run("clear", shell=True, check=True)

player1 = Piece("Foo","red", "O", "1")
player2 = Piece("Bar","blue", "X", "2")
board = Board()

for i in range(3):
    board.display()
    player1_column = int(input("P1 Turn: "))
    player1.drop(board, player1_column)
    player2_column = int(input("P2 Turn: "))
    player2.drop(board, player2_column)
    clear_screen()


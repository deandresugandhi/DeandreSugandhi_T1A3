from game_board import Board, Piece
from win_conditions import VictoryChecker
from game_engine import game_start

board = Board()
player1 = Piece("Foo","red", "O", "1")
player2 = Piece("Bar","blue", "X", "2")
referee = VictoryChecker(board, player1, player2)

game_start(board, player1, player2, referee)




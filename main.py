from game_board import Board, Piece
from win_conditions import VictoryChecker
from game_engine import game_start

player1 = Piece("Foo","red", "O", "1")
player2 = Piece("Bar","blue", "X", "2")
players = [player1, player2]
board = Board(players)
referee = VictoryChecker(board, player1, player2)

game_start(board, players, referee)




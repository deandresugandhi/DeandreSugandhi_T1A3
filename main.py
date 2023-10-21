from game_board import Board, Piece
from win_conditions import VictoryChecker
from game_engine import game_in_progress, game_complete

player1 = Piece("Player 1","red", "O", "1")
player2 = Piece("Player 2","blue", "X", "2")
players = [player1, player2]
board = Board(players)
referee = VictoryChecker(board, player1, player2)


player1.color = "yellow" 

game_result = game_in_progress(board, players, referee)
game_complete(game_result)



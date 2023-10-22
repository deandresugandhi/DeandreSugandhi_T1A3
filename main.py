from game_board import Board, Piece
from win_conditions import VictoryChecker
from game_engine import game_in_progress, game_complete
from start_menu import game_setup

player1 = Piece("Player1","white", "O", "1")
player2 = Piece("Player2","white", "X", "2")
players = [player1, player2]
user1 = User("Guest", )
user2 = User()
board = Board(players)
referee = VictoryChecker(board, player1, player2)

game_setup(player1)
game_setup(player2)

game_result = game_in_progress(board, players, referee)
game_complete(game_result)



from game_board import Board, Piece
from win_conditions import VictoryChecker
from game_engine import game_in_progress, game_complete, game_reset
from start_menu import game_setup, game_start
from user_utils import User

player1 = Piece("Player1","white", "O", "1")
player2 = Piece("Player2","white", "X", "2")
players = [player1, player2]
user1 = User("Guest", games_played=None, wins=None, losses=None, win_ratio=None)
user2 = User("Guest", games_played=None, wins=None, losses=None, win_ratio=None)
users = [user1, user2]
board = Board(players)
referee = VictoryChecker(board, players)

game_setup(player1, user1)
game_setup(player2, user2)
game_start(players)

while True:
    game_result = game_in_progress(board, players, referee)
    post_game = game_complete(game_result, users)
    if post_game.lower() == "y":
        game_reset(board, players)
        continue
    else:
        break



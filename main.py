
# Standard Library Modules
# Third-party library Modules
# Local Modules
from game_board import Board, Piece
from win_conditions import VictoryChecker
from game_engine import game_in_progress, game_complete, game_reset
from start_menu import game_setup, start_screen, MainLobby
from user_utils import User, reset_login
from player_lounge import generate_users_record, PlayerLounge
from utilities import validate_input
import atexit
import colorama

reset_login()
atexit.register(reset_login)
colorama.init(autoreset=True)

player1 = Piece("Guest1","white", "O", "1")
player2 = Piece("Guest2","white", "X", "2")
players = [player1, player2]
user1 = User("Guest", games_played=None, wins=None, losses=None, win_ratio=None)
user2 = User("Guest", games_played=None, wins=None, losses=None, win_ratio=None)
users = [user1, user2]
board = Board(players)
referee = VictoryChecker(board, players)
main_lobby = MainLobby()
users_record = generate_users_record()
player_lounge = PlayerLounge(users_record)

start_screen()
print("Welcome! Before starting the game, both players must be logged in.")
game_setup(player1, user1)
game_setup(player2, user2)

while True:
    move_to = main_lobby.enter()

    match move_to:
        case "lounge":
            player_lounge.enter(players)
            continue
        case "match":
            while True:
                game_result = game_in_progress(board, players, referee)
                post_game = game_complete(game_result, users)
                if post_game.lower() == "y":
                    game_reset(board, players)
                    continue
                else:
                    break
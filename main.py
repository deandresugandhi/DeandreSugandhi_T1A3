"""
Module from which the program will be executed.
"""


# Third-party library Modules
import atexit
import colorama

# Local Modules
from game_board import Board, Piece
from win_conditions import VictoryChecker
from game_engine import game_in_progress, game_complete, game_reset, game_start
from start_menu import game_setup, start_screen
from user_utils import User, reset_log, generate_users_record, check_json
from hubs import PlayerLounge, MainLobby


# Start program by ensuring users.json file and is in the right format,
# and logging all players out as a fail-safe
check_json()
reset_log()
# Log all players out when program exits.
atexit.register(reset_log)
# Colorama.init ensures termcolor also works on Windows and other systems.
colorama.init(autoreset=True)

# Player pieces. Defaults to guest pieces.
player1 = Piece("Guest1","white", "O", "1")
player2 = Piece("Guest2","white", "X", "2")
players = [player1, player2]
# User accounts. Defaults to guest accounts.
user1 = User("Guest", games_played=None, wins=None, losses=None, win_ratio=None)
user2 = User("Guest", games_played=None, wins=None, losses=None, win_ratio=None)
users = [user1, user2]
# Game board object where game is played.
board = Board(players)
# Referee checking wining condition.
referee = VictoryChecker(board, players)
# Game hubs used throughout the program.
main_lobby = MainLobby()
users_record = generate_users_record()
player_lounge = PlayerLounge(users_record)


start_screen()
print("Welcome! Before starting the game, both players must be logged in.")
game_setup(player1, user1)
game_setup(player2, user2)
# Main functionalities of the game. Loops indefinitely. Exit lobby quits game.
while True:
    # Enters main lobby, loop until user exits or move to other hub. Exit lobby
    # quits game.
    move_to = main_lobby.enter()
    match move_to:
        case "lounge":
            # Enters player lounge, loop until user exits lounge or move to
            # other hub.
            player_lounge.enter(players)
            continue
        case "match":
            # Starts match loop
            while True:
                game_start(players)
                game_result = game_in_progress(board, players, referee)
                post_game = game_complete(game_result, users)
                if post_game.lower() == "y":
                    game_reset(board, players)
                    continue
                break

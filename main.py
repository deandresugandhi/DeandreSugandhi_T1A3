from game_board import Board, Piece
from win_conditions import VictoryChecker
from game_engine import game_in_progress, game_complete, game_reset
from start_menu import game_setup, game_start, start_screen, lobby
from user_utils import User, reset_login
from player_lounge import generate_users_record, PlayerLounge
from utilities import validate_input
import atexit
import colorama

colorama.init(autoreset=True)

reset_login()

player1 = Piece("Player1","white", "O", "1")
player2 = Piece("Player2","white", "X", "2")
players = [player1, player2]
user1 = User("Guest", games_played=None, wins=None, losses=None, win_ratio=None)
user2 = User("Guest", games_played=None, wins=None, losses=None, win_ratio=None)
users = [user1, user2]
board = Board(players)
referee = VictoryChecker(board, players)
users_record = generate_users_record()
player_lounge = PlayerLounge(users_record)

start_screen()
game_setup(player1, user1)
game_setup(player2, user2)
command = lobby()
match command:
    case "lounge":
        command = player_lounge.enter_lounge()
        match command:
            case "high-score":
                command = validate_input
                player_lounge.display_high_scorer()
            case "customize":

            case "player-info":
            
            case "exit":

    case "match":
    
    case "exit":

game_start(players)

while True:
    game_result = game_in_progress(board, players, referee)
    post_game = game_complete(game_result, users)
    if post_game.lower() == "y":
        game_reset(board, players)
        continue
    else:
        break

board.display()

atexit.register(reset_login)
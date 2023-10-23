from utilities import clear_screen, reset_screen, validate_input
from termcolor import colored
from custom_errors import ColumnFullError
import re


def validate_player_turn(prompt, match, board, players):
    user_input = input(prompt)
    while True:
        if re.fullmatch(match, user_input):
            clear_screen()
            return user_input
        else:
            user_input = input(message) if masked == False else askpass(message)
            "^([1-7]|clear|surrender)$",
def game_in_progress(board, players, referee):
    player_turn = 0
    move_count = 0

    while referee.check_victory() is None and move_count < 42:
        reset_screen(board)
        player_command = input(f"\n{colored(players[player_turn].player_name, players[player_turn].color)}'s turn: ")
        while True:
            if re.fullmatch( "^([1-7]|clear|surrender)$", player_command):
                if player_command.isdigit():
                    try:
                        players[player_turn].drop(board, int(player_command))
                    except ColumnFullError as error:
                        player_command = input(error)
                    else:
                        player_turn = int(not player_turn)
                        move_count += 1
                        break        
                elif player_command.lower() == "clear":
                    board.clear_board()
                    player_turn = 0
                    break
                elif player_command.lower() == "surrender":
                    players[player_turn].surrender = True
                    reset_screen(board)
                    return referee.check_victory(), players[player_turn]
            else:
                player_command = input("Invalid input, please try again: ")

    reset_screen(board)
    return referee.check_victory(), None


def game_complete(game_result, users):
    winner, surrendered = game_result
    if winner is None:
        print("Game Draw!")
    else:
        if surrendered is not None:
            print(f"{surrendered.player_name} surrendered!") 
        print(f"{winner.player_name} wins!")
        
    users[0].update_game_history(winner)
    users[1].update_game_history(winner)

    play_again = validate_input("Play again? (y / n): ","^[yn]$")
    return play_again

def game_reset(board, players):
    board.clear_board()
    players[0].surrender = False
    players[1].surrender = False

    

    




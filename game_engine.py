from game_board import Board
from win_conditions import VictoryChecker
import subprocess

def game_in_progress(board, players, referee):
    def clear_screen():
        try:
            subprocess.run("cls", shell=True, check=True)
        except subprocess.CalledProcessError:
            subprocess.run("clear", shell=True, check=True)

    def reset_screen(board):
        clear_screen()
        board.display()

    player_turn = 0
    move_count = 0

    while referee.check_victory() is None and move_count < 42:
        reset_screen(board)
        player_command = input(f"{players[player_turn]._player_name}'s turn: ")
        if player_command.lower() == "clear":
            board.clear_board()
            player_turn = 0
            continue
        elif player_command.lower() == "surrender":
            players[player_turn].surrender = True
            reset_screen(board)
            return referee.check_victory(), players[player_turn]._player_name
        players[player_turn].drop(board, int(player_command))
        player_turn = int(not player_turn)
        move_count += 1
        continue
    reset_screen(board)
    return referee.check_victory(), None


def game_complete(game_result):
    winner, surrendered = game_result
    if winner is None and surrendered is None:
        print("Game Draw!")
    else:
        if surrendered is not None:
            print(f"{game_result[1]} surrendered!") 
        print(f"{game_result[0]} wins!")


from game_board import Board
from win_conditions import VictoryChecker
import subprocess

def game_start(board, players, referee):
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
            player_turn = int(not player_turn)
            continue
        players[player_turn].drop(board, int(player_command))
        player_turn = int(not player_turn)
        move_count += 1
        continue

    reset_screen(board)
    print(f"{referee.check_victory()} wins the match!") if move_count < 42 else print("Game Draw!")

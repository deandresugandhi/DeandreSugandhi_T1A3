from game_board import Board
import subprocess

def game_start(board, player1, player2, referee):
    def clear_screen():
        try:
            subprocess.run("cls", shell=True, check=True)
        except subprocess.CalledProcessError:
            subprocess.run("clear", shell=True, check=True)

    def reset_screen(board):
        clear_screen()
        board.display()

    player_turn = 1
    while referee.check_victory() is None:
        reset_screen(board)
        if player_turn == 1:
            p1_command = input("P1 Turn: ")
            if p1_command.lower() == "clear":
                board.clear_board()
                continue
            player1.drop(board, int(p1_command))
            player_turn = 2
            continue
        elif player_turn == 2:
            p2_command = input("P2 Turn: ")
            if p2_command.lower() == "clear":
                board.clear_board()
                continue
            player2.drop(board, int(p2_command))
            player_turn = 1
            continue
    reset_screen(board)
    print(f"{referee.check_victory()} wins the match!")

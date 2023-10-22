import subprocess
import re


def clear_screen():
    try:
        subprocess.run("cls", shell=True, check=True)
    except subprocess.CalledProcessError:
        subprocess.run("clear", shell=True, check=True)

def reset_screen(board):
    clear_screen()
    board.display()

def validate_input(prompt, match, message="Invalid input, please try again: "):
        user_input = input(prompt)
        while True:
            if re.fullmatch(match, user_input):
                clear_screen()
                return user_input
            else:
                user_input = input(message)
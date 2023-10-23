import subprocess
import re
from maskpass import askpass


def clear_screen():
    try:
        subprocess.run("cls", shell=True, check=True)
    except subprocess.CalledProcessError:
        subprocess.run("clear", shell=True, check=True)

def reset_screen(board):
    clear_screen()
    board.display()

def validate_input(prompt, match, message="Invalid input, please try again: ", masked = False, case_sensitive = False):
    user_input = input(prompt) if masked == False else askpass(prompt)
    while True:
        if case_sensitive == False:
            if re.fullmatch(match, user_input.lower()):
                clear_screen()
                return user_input
        else:
            if re.fullmatch(match, user_input):
                clear_screen()
                return user_input
        user_input = input(message) if masked == False else askpass(message)


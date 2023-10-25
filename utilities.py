import subprocess
import re
from maskpass import askpass
from termcolor import colored
import json


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

def validate_color(prompt):
    user_input = input(prompt)
    while True:
        try:
            colored("test", user_input)
        except:
            user_input = input("Invalid color, please try again: ")
        else:
            clear_screen()
            return user_input

def update_attributes(piece, user, details):
    piece.player_name = details.get("username")
    piece.color = details.get("color")
    piece.piece_type = details.get("piece_type")
    user.username = details.get("username")
    user.games_played = details.get("games_played")
    user.wins = details.get("wins") 
    user.losses = details.get("losses")
    user.win_ratio = details.get("win_ratio")

def change_piece_properties(player):
    if player.player_name.lower() in ["guest", "guest1", "guest2"]:
        print("Guest accounts cannot customize pieces.")
    else:
        while True:
            player.color = validate_color(
                ("Pick your piece color.\n"
                "Available options: black, red, green, yellow, blue, magenta, cyan, light_grey, "
                "dark_grey, light_red, light_green, light_yellow, light_blue, light_magenta, light_cyan.\n"
                f"{player.player_name}'s new color: "),
            )

            player.piece_type = validate_input(
                ("Pick your piece type.\n"
                "Your piece type can only contain a single uppercase (A-Z) or lowercase letter(a-z), or a single number(0-9).\n"
                "Piece Type: "),
                "^[a-zA-Z0-9]$",
                "Invalid piece type, please try again: ",
                case_sensitive = True
            )

            print(f"preview: {colored(player.piece_type, player.color)}")
            
            piece_satisfied = validate_input(
                ("Confirm piece type and color? \n" 
                "(y / n): "),
                "^(y|n)$"
            )

            clear_screen() 
            if piece_satisfied == "n":
                continue 
            else:
                break

        with open("users.json", "r") as file:
            users = json.load(file)

        for user in users:
            if user["username"] == player.player_name:
                user["color"] = player.color
                user["piece_type"] = player.piece_type
                break
                
        with open("users.json", "w") as file:
            json.dump(users, file, indent=4)



            
import re
import subprocess
import json
import colorama
from termcolor import colored

def clear_screen():
    try:
        subprocess.run("cls", shell=True, check=True)
    except subprocess.CalledProcessError:
        subprocess.run("clear", shell=True, check=True)


def game_setup(player):

    def validate_input(prompt, match, message="Invalid input, please try again: "):
        user_input = input(prompt)
        while True:
            if re.fullmatch(match, user_input):
                clear_screen()
                return user_input
            else:
                user_input = input(message)

    def validate_color(prompt):
        user_input = input(prompt)
        while True:
            try:
                colored("test", user_input)
            except:
                user_input = input("Invalid color, please try again: ")
            else:
                return user_input

    def validate_username(prompt, match):
        user_input = input(prompt)
        with open("users.json", "r") as file:
            users = json.load(file)
    
        while True:
            if not re.fullmatch(match, user_input):
                user_input = input("Invalid username, please try again: ")
                continue

            for user in users:
                if user_input == user.get("username"):
                    user_input = input(f"Username {user_input} is taken, please try again: ")
                    break
            else:
                clear_screen()
                return user_input
            
    def store_account(username, pin, color, piece_type):
        user_data = {
            "username": username,
            "pin": pin,
            "games-played": 0,
            "wins": 0,
            "losses": 0,
            "win-ratio": 0,
            "color": color,
            "piece_type": piece_type,
            "logged_in": False
        }
        with open("users.json", "r") as file:
            users = json.load(file)

        users.append(user_data)

        with open("users.json", "w") as file:
            json.dump(users, file, indent=4)
    

    def validate_account(username, pin):
        with open("users.json", "r") as file:
            users = json.load(file)
        for user in users:
            if username == user.get("username"):
                if pin == user["pin"]:
                    user["logged_in"] = True 
                    return user
        return None



    is_existing_user = validate_input(
        (f"Player {player.player}! Are you an existing user? (y / n): "),
        "^[yn]$"
    )

    if is_existing_user.lower() == "n":
        account_type = validate_input(
            ("Do you want to create a new account or use a guest account?\n"
            "Note: Create an account if you want to be recorded in the high-score board, "
            "customize your game piece, and have access to your own game stats. \n" 
            "(new / guest): "),
            "^(new|guest)$"
        )

        if account_type.lower() == "new":
            new_username = validate_username(
                ("Please create a username for your account. This will also be your display name. \n"
                "1. Usernames can only contain uppercase (A-Z) or lowercase "
                "letters (a-z), numbers(0-9), periods (.), and underscores (_).\n"
                "2. Usernames cannot start or end with a period(.) or underscore(.).\n"
                "3. Usernames should be between 5 - 20 characters long.\n"
                "Username: "),
                "^[a-zA-Z0-9][a-zA-Z0-9._-]{3,18}[a-zA-Z0-9]$",
            )

            new_pin = validate_input(
                "Please enter a 4-digit PIN for your account. This will be used to verify your future sign-ins. \n"
                "Note: For now, PINS and usernames are stored in a .json file, which is a human-readable file format. Due to the risk "
                "of unauthorized access, please use a unique PIN that is not associated with your other external accounts.\n"
                "PIN: ",
                r"^\d{4}$",
                "Invalid PIN, please try again: "
            )

            new_player_color = validate_color(
                ("Pick your piece color.\n"
                "Your piece color determines the color of your piece on the board. "
                "Available options: black, red, green, yellow, blue, magenta, cyan, light_grey, "
                "dark_grey, light_red, light_green, light_yellow, light_blue, light_magenta, light_cyan.\n"
                "Color: "),
            )
            
            new_player_piece_type = validate_input(
                ("Pick your piece type.\n"
                "Your piece type determines the form that represents your piece on the board. "
                "It can only contain a single uppercase (A-Z) or lowercase letter(a-z), or a single number(0-9).\n"
                "Piece Type: "),
                "^[a-zA-Z0-9]$",
                "Invalid piece type, please try again: "
            )

            store_account(new_username, new_pin, new_player_color, new_player_piece_type)
            player.player_name = new_username
            player.color = new_player_color
            player.piece_type = new_player_piece_type

            print(f"Your account has been created! You will be playing as {new_username}")

        
        elif account_type.lower() == "guest":
            print(f"Using guest account. You will be playing as {player.player_name}.")

    elif is_existing_user.lower() == "y":
        while True:
            existing_username = input("Enter your username: ")
            existing_pin = input("Enter your PIN: ")
            account_details = validate_account(existing_username, existing_pin)

            if account_details == None:
                print("Invalid username or PIN. Please try again.")
            else:
                player.player_name = account_details.get("username")
                player.color = account_details.get("color")
                player.piece_type = account_details.get("piece_type")
                print(f"Successfully logged in! You will be playing as {colored(player.player_name, player.color)}.")
                break
            


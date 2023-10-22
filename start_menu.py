import re
import subprocess
import json

def validate_input(prompt, match = ".*", message = "Invalid input, please try again."):
    while True:
        try:
            user_input = input(prompt)
        except ValueError as error_message:
            print(error_message)
        else:
            if re.fullmatch(match, user_input):
                return user_input
            print(message)

        
def game_setup(player):
    def clear_screen():
        try:
            subprocess.run("cls", shell=True, check=True)
        except subprocess.CalledProcessError:
            subprocess.run("clear", shell=True, check=True)

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
        }
        with open("users.json", "a") as file:
            json.dump(user_data, file)

    existing_user = validate_input(
        (f"Player {player.player}! Are you an existing user? (y / n)",
        "^[yn]$"),
    )

    if existing_user.lower() == "n":
        account_type = validate_input(
            ("Do you want to create a new account or use a guest account?\n"
            "Note: Create an account if you want to be recorded in the high-score board, "
            "customize your game piece, and have access to your own game stats. \n" 
            "(new / guest): "),
            "^(new|guest)$",
        )

        if account_type.lower() == "new":
            player.player_name = validate_input(
                "Please create a username for your account. This will also be your display name. \n"
                "1. Usernames can only contain uppercase (A-Z) or lowercase "
                "letters (a-z), numbers(0-9), periods (.), and underscores (_).\n"
                "2. Usernames cannot start or end with a period(.) or underscore(.).\n"
                "3. Usernames should be between 5 - 20 characters long.\n"
                "Username: "
            )
            new_username = player.player_name

            new_pin = validate_input(
                "Please enter a 4-digit PIN for your account. This will be used to verify your future sign-ins. \n"
                "Note: For now, PINS and usernames are stored in a .json file, which is a human-readable file format. Due to the risk "
                "of unauthorized access, please use a unique PIN that is not associated with your other external accounts.\n"
                "PIN: ",
                "r'^\d{4}$'",
                "Invalid PIN, please try again."
            )

            player.color = validate_input(
                "Pick your piece color.\n"
                "Your piece color determines the color of your piece on the board."
                "Available options: black, red, green, yellow, blue, magenta, cyan, light_grey, "
                "dark_grey, light_red, light_green, light_yellow, light_blue, light_magenta, light_cyan"
                "Color: "
            )
            new_player_color = player.color
            
            player.piece_type = validate_input(
                "Pick your piece type.\n"
                "Your piece type determines the form that represents your piece on the board."
                "It can only contain a single uppercase (A-Z) or lowercase letter(a-z), or a single number(0-9)."
            )
            new_player_piece_type = player.piece_type

            print(f"Your account has been created! You will be playing as {new_username}")

        
        elif account_type.lower() == "guest":
            print(f"You will be playing as a guest. Your name is {player.player_name}.")


    elif existing_user == "existing":
        existing_username = validate_input(
            "Please enter your username: ",
        )

        existing_pin = validate_input(
            "Please enter your PIN: ",
        )


    
    elif player_status == "existing":
        player.color = validate_input("Pick your piece color")

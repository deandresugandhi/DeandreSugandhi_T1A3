import re
import json
from termcolor import colored
from utilities import clear_screen, validate_input, update_attributes, change_piece_properties, validate_color
import art
from maskpass import askpass

def start_screen():
    clear_screen()
    logo1 = colored(art.text2art("CONNECT", font="chunky", space = 0), "blue")
    logo2 = colored(art.text2art("FOUR", font="coinstak", space = 5)[0:-40], "red", attrs=["bold"])
    frame = colored("=" * 61, "yellow", attrs=["underline"])
    frame2 = colored('-' * 25, "yellow")
    text = colored(" TERMINAL ", "dark_grey", attrs=["bold"])
    print("\n" + frame2 + text + frame2 + colored('-', "yellow"))
    print(logo1 + logo2)
    print(frame + "\n")
    input(f"{' ' * 16} Press Enter to continue!")
    clear_screen()

def lobby():
    loun = colored("LOUNGE", "blue")
    mat = colored("MATCH", "green")
    ex = colored("EXIT", "red")
    print(fr'''
        \_                                                _/
          \_                                            _/
            \                                      ____/
            |                                     |
            |______                         ______|
            |      |\ ___________________ /|      |      
            |      | |     _________     | |      |
            |      | |    |    |    |    | |      |
            |{loun}| |    |    |    |    | | {ex} |
            | <--- | |    |   o|o   |    | | ---> |       
            |      | |    |    |    |    | |      |
            |      | |____|____|____|____| |      |
            |______|/        {mat}        \|______|
            |                  .                  |
        ____|                 / \                 |___
      _/                     / | \                    \_
     /                         |                        \
                               |                               
    ''')
    command = validate_input(
        "Welcome to Terminal Connect Four! Select an option:\n"
        "LOUNGE: Customize your piece, or view player statistics\n"
        "MATCH: Start a player match\n"
        "EXIT: All users logout and exit the game\n"
        "(lounge / match / exit): ",
        "^(lounge|match|exit)$"
    )
    return command.lower()

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
        "games_played": 0,
        "wins": 0,
        "losses": 0,
        "win_ratio": 0,
        "color": color,
        "piece_type": piece_type,
        "logged_in": "y"
    }
    with open("users.json", "r") as file:
        users = json.load(file)

    users.append(user_data)

    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)
    
    return user_data

def validate_account(username, pin):
    with open("users.json", "r") as file:
        users = json.load(file)
    for user in users:
        if username == user.get("username") and pin == user.get("pin"):
            if user.get("logged_in") == "y":
                return "Duplicate"
            else:
                user["logged_in"] = "y"
                with open("users.json", "w") as file:
                    json.dump(users, file, indent=4) 
                return user
    return None

def game_setup(player, user):
    is_existing_user = validate_input(
        ("Welcome! Before starting the game, both players must be logged in."
        f"Player {player.player}! Are you an existing user? (y / n): "),
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
                "Invalid PIN, please try again: ",
                masked = True
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
                "Invalid piece type, please try again: ",
                case_sensitive = True
            )

            account_details = store_account(new_username, new_pin, new_player_color, new_player_piece_type)
            update_attributes(player, user, account_details)

            print(f"Your account has been created! You will be playing as {new_username}")

        
        elif account_type.lower() == "guest":
            print(f"Using guest account. You will be playing as {player.player_name}.")

    else:
        while True:
            existing_username = input("Enter your username: ")
            existing_pin = askpass("Enter your PIN: ")
            account_details = validate_account(existing_username, existing_pin)

            if account_details == None:
                print("Invalid username or PIN. Please try again: ")
            elif account_details == "Duplicate":
                print(f"{existing_username} is already logged in. Please try again: ")
            else:
                update_attributes(player, user, account_details)
                print(f"Successfully logged in! You will be playing as {colored(player.player_name, player.color)}.")
                break
    
def game_start(players):
    def ask_to_change_piece_properties(player):
        player_changing = validate_input(
            (f"Does {player.player_name} want to change piece properties?\n"
            "(y / n): "),
            "^(y|n)$"
        )

        if player_changing == "y":
            change_piece_properties(player)
        else:
            pass

    clear_screen()

    while players[0].color == players[1].color and players[0].piece_type == players[1].piece_type:
        print("In order to start the game, both players cannot have the exact same piece type and color. Please change piece type / color accordingly.")
        ask_to_change_piece_properties(players[0])
        ask_to_change_piece_properties(players[1])
        
    ready = input(f"{colored(players[0].player_name, players[0].color)} and {colored(players[1].player_name, players[1].color)}, press enter when ready! ")



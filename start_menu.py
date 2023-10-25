# Standard Library Modules
import re
import json

#Third-party Library Modules
from termcolor import colored
import art
from maskpass import askpass

# Local Modules
from utilities import (
    clear_screen,
    validate_input,
    update_attributes,
    validate_color
)


def start_screen():
    """
    Function that defines how the start screen of the game works and is
    displayed. Includes the main logo of the game, which appears right after a
    user accesses the app.
    """
    clear_screen()
    # Generates ASCII art of the main logo of the game.
    logo1 = colored(art.text2art("CONNECT", font="chunky", space = 0), "blue")
    logo2 = colored(art.text2art("FOUR", font="coinstak", space = 5)[0:-40], "red", attrs=["bold"])
    frame = colored("=" * 61, "yellow", attrs=["underline"])
    frame2 = colored('-' * 25, "yellow")
    text = colored(" TERMINAL ", "dark_grey", attrs=["bold"])

    # Displays the ASCII art
    print("\n" + frame2 + text + frame2 + colored('-', "yellow"))
    print(logo1 + logo2)
    print(frame + "\n")
    input(f"{' ' * 16} Press Enter to continue!")

    clear_screen()


def validate_username(prompt, match):
    """
    Function to define how username validation works. Input loops until player
    enters a valid username format.

    Args:
    1. prompt (str): The prompt that will be displayed to the user to input
       username.
    2. match (str): The regular expression (RegEx) that will be used to validate 
       username.
    """
    user_input = input(prompt)
    with open("users.json", "r", encoding="utf-8") as file:
        users = json.load(file)

    # Loops until a valid username format is entered.
    while True:
        # Matches to the username format.
        if not re.fullmatch(match, user_input):
            user_input = input("Invalid username, please try again: ")
            continue
        # If username is in the right format, but is the name of a guest
        # account, loop starts again.
        if user_input.lower == "guest" or "guest1" or "guest2":
            user_input = input("That's a guest account. Please try again: ")
            continue
        # If username is in the right format and is not a guest account, but
        # there is another user account associated with it, loop starts again.
        for user in users:
            if user_input == user.get("username"):
                user_input = input(f"Username {user_input} is taken, please try again: ")
                break
        else:
            clear_screen()
            return user_input


def store_account(username, pin, color, piece_type):
    """
    Function to define how accounts are stored. Each account is stored as a 
    dictionary with account details in the users.json file. The user.json file 
    is a list with all the generated user dictionaries.

    Args:
    1. username (str): The username to be stored in the user dictionary.
    2. pin (str): The pin to be associated with the account.
    3. color (str): The Piece color associated with the account.
    4. piece_type (str): The Piece type associated with the account.
    """
    # Determines how a user dictionary is formatted.
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
    # Reads users.json, appends a user dictionary, and writes them to the file.
    with open("users.json", "r", encoding="utf-8") as file:
        users = json.load(file)
    users.append(user_data)
    with open("users.json", "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4)

    return user_data


def validate_account(username, pin):
    """
    Function to define how user login is validated. Accesses user.json to make
    sure username and pin match with a user's record.

    Args:
    1. username (str): The username to be validated.
    2. pin (str): The pin to be validated.
    """
    with open("users.json", "r", encoding="utf-8") as file:
        users = json.load(file)
    # Matches username and pin with user records.
    for user in users:
        if username == user.get("username") and pin == user.get("pin"):
            # Invalidate login attempt when the associated user is currently
            # logged in.
            if user.get("logged_in") == "y":
                return "Duplicate"
            # When username and pin is validated, user is set to logged in.
            user["logged_in"] = "y"
            with open("users.json", "w", encoding="utf-4") as file:
                json.dump(users, file, encoding="utf-4", indent=4)

            return user
    # If username and pin combination is not found, invalidates login attempt.
    return None


def game_setup(player, user):
    """
    Function to define how the players are setup before accessing the main
    functionalities of the game. Players can login to their user accounts if
    they have previously created them, create a new account if they wish to,
    or use a guest account if they want to play the game without their own
    account. Several game functionalities are only available for those using
    user accounts.

    Args:
    1. player (Piece): The Piece instance that is to be modified through player
       login.
    2. user (User): The User instance that will be modified through player
       login.
    """
    is_existing_user = validate_input(
        (f"Player {player.player}! Are you an existing user? (y / n): "),
        "^[yn]$"
    )

    # If a player is a new user, they can choose to create a new account. or a
    # guest account.
    if is_existing_user.lower() == "n":
        account_type = validate_input(
            ("Do you want to create a new account or use a guest account?\n"
            "Note: Create an account if you want to be recorded "
            "in the high-score board, "
            "customize your game piece, and have access to your own game stats.\n" 
            "(new / guest): "),
            "^(new|guest)$"
        )

        # Account creation start. Each user detail input is looped until they
        # match their respective uniquely defined format.
        if account_type.lower() == "new":
            new_username = validate_username(
                ("Please create a username for your account. This will also be "
                "your display name. \n"
                "1. Usernames can only contain uppercase (A-Z) or lowercase "
                "letters (a-z), numbers(0-9), periods (.), and underscores (_).\n"
                "2. Usernames cannot start or end with a period(.) or underscore(.).\n"
                "3. Usernames should be between 5 - 20 characters long.\n"
                "Username: "),
                "^[a-zA-Z0-9][a-zA-Z0-9._-]{3,18}[a-zA-Z0-9]$",
            )
            # For now, pins are not encrypted when stored in the users.json.
            # User is warned because a person having access to users.json can
            # easily read all users' login details, including pins.
            new_pin = validate_input(
                "Please enter a 4-digit PIN for your account. "
                "This will be used to verify your future sign-ins.\n"
                "Note: For now, PINS and usernames are stored in a .json file,"
                "which is a human-readable file format. Due to the risk "
                "of unauthorized access, please use a unique PIN that is not "
                "associated with your other external accounts.\n"
                "PIN: ",
                r"^\d{4}$",
                "Invalid PIN, please try again: ",
                # Each character of the input will be masked with a "*".
                masked = True
            )

            new_player_color = validate_color(
                ("Pick your piece color.\n"
                "Your piece color determines the color of your piece on the board. "
                "Available options: black, red, green, yellow, blue, magenta, "
                "cyan, light_grey, dark_grey, light_red, light_green, "
                "light_yellow, light_blue, light_magenta, light_cyan.\n"
                "Color: "),
            )
            
            new_player_piece_type = validate_input(
                ("Pick your piece type.\n"
                "Your piece type determines the form that represents your "
                "piece on the board. "
                "It can only contain a single uppercase (A-Z) or lowercase "
                "letter(a-z), or a single number(0-9).\n"
                "Piece Type: "),
                "^[a-zA-Z0-9]$",
                "Invalid piece type, please try again: ",
                case_sensitive = True
            )

            # Once all input are validated, account is stored in the .json file,
            # and current user dictionary is assigned to account_details
            # variable.
            account_details = store_account(
                new_username,
                new_pin,
                new_player_color,
                new_player_piece_type
            )

            update_attributes(player, user, account_details)

            print(f"Your account has been created! You will be playing as {new_username}")

        # If they don't want to create a new account, a guest account is used.
        elif account_type.lower() == "guest":
            print(f"Using guest account. You will be playing as {player.player_name}.")
      
        input("Press enter to continue!")
        clear_screen()

    # If they are an existing user, they can login to their user account.
    else:
        while True:
            existing_username = input("Enter your username: ")
            existing_pin = askpass("Enter your PIN: ")
            account_details = validate_account(existing_username, existing_pin)

            if account_details == None:
                try_again = validate_input(
                    ("Invalid username or PIN. Try again or use a guest account?\n"
                     "(again / guest): "),
                     "^(again|guest)$"
                )
                if try_again.lower() == "again":
                    continue
                elif try_again.lower() == "guest":
                    print(f"Using guest account. You will be playing as {player.player_name}")
                    break
            
            elif account_details == "Duplicate":
                print(f"{existing_username} is already logged in. Please try again: ")
            else:
                update_attributes(player, user, account_details)
                print(f"Successfully logged in! You will be playing as {colored(player.player_name, player.color)}.")
                input("Press enter to continue!")
                clear_screen()
                break
    




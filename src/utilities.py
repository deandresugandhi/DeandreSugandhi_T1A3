"""
Module that contains utility functions for general use by other modules of the
program.
"""


# Standard Library Modules
import re
import subprocess
import json

# Third-party Library Modules
from maskpass import askpass
from termcolor import colored

# Local Modules
from custom_errors import InvalidCommandError, UsernameError, ColorError


def clear_screen():
    """A function that clears the terminal."""
    try:
        subprocess.run("cls", shell=True, check=True)
    except subprocess.CalledProcessError:
        subprocess.run("clear", shell=True, check=True)


def reset_screen(board):
    """A function that clears the terminal, and displays updated game board."""
    clear_screen()
    board.display()


def validate_input(
        prompt,
        match,
        message="Invalid command, please try again: ",
        masked = False,
        case_sensitive = False
    ):
    """
    A function that checks a user input to ensure they match a given RegEx
    pattern. Loops until valid input is made.

    Args:
    1. prompt (str): The prompt to displayed to the user to type in an input.
    2. match (str): The RegEx pattern to match the user input.
    3. message (str): The message to display to the user if the input does not
       match the RegEx pattern.
    4. masked (bool): Defines whether the input will be masked using the
       maskpass module.
    5. case_sensitive (bool): Defines whether the input is case sensitive.

    Returns the user input once it is considered valid.
    """
    user_input = input(prompt) if masked is False else askpass(prompt)
    while True:
        try:
            if case_sensitive is False:
                if re.fullmatch(match, user_input.lower()):
                    clear_screen()
                    return user_input
            else:
                if re.fullmatch(match, user_input):
                    clear_screen()
                    return user_input
            raise InvalidCommandError(message)
        # Ask for input with a different prompt (message) if input is invalid
        except InvalidCommandError as error:
            user_input = input(error) if masked is False else askpass(error)


def validate_username(prompt, match):
    """
    Function to define how username validation works. Input loops until player
    enters a valid username format.

    Args:
    1. prompt (str): The prompt that will be displayed to the user to input
       username.
    2. match (str): The regular expression (RegEx) that will be used to validate 
       username.

    Returns the user input once it is considered valid.
    """
    user_input = input(prompt)
    with open("users.json", "r", encoding="utf-8") as file:
        users = json.load(file)

    # Loops until a valid username format is entered.
    while True:
        try:
        # Matches to the username format.
            if not re.fullmatch(match, user_input):
                raise UsernameError("Invalid username, please try again: ")
            # If username has right format, but is guest, loops again.
            if user_input.lower in ("guest", "guest1", "guest2"):
                raise UsernameError("That's a guest account, please try again: ")
            # If username has right format and is not guest, but is associated
            # with another user account, loops again.
            for user in users:
                if user_input == user.get("username"):
                    raise UsernameError(f"Username {user_input} is taken, "
                                        "please try again: ")
            clear_screen()
            return user_input
        except UsernameError as error:
            user_input = input(error)


def validate_color(prompt):
    """
    Function to define how color validation works. Input loops until player
    enters a valid color format.

    Args:
    1. prompt (str): The prompt that will be displayed to the user to input
       color.

    Returns the user input once it is considered valid.
    """
    user_input = input(prompt)
    while True:
        try:
            try:
                colored("test", user_input)
            # Termcolor raises KeyError if it fails to color the string using
            # the inputted value.
            except KeyError as exc:
                raise ColorError("Invalid color, please try again: ") from exc
            else:
                clear_screen()
                return user_input
        except ColorError as error:
            user_input = input(error)


def update_attributes(piece, user, details):
    """
    Function to update the Piece and User instance using the details read from
    users.json.

    Args:
    1. piece (Piece): The Piece instance whose attributes are being updated.
    2. user (User): The User instance whose attributes are being updated.
    3. details (dict): The dictionary storing a user's details from which to
       update the Piece and User instances.
    """
    piece.player_name = details.get("username")
    piece.color = details.get("color")
    piece.piece_type = details.get("piece_type")
    user.username = details.get("username")
    user.games_played = details.get("games_played")
    user.wins = details.get("wins")
    user.losses = details.get("losses")
    user.win_ratio = details.get("win_ratio")


def change_piece_properties(player):
    """
    Function to modify the attributes of a Piece instance, namely its color and
    piece type. Input loops until player enters a valid color and piece.

    Args:
    1. player (Piece): The Piece instance whose attributes are being modified.
    """
    if player.player_name.lower() in ["guest", "guest1", "guest2"]:
        print("Guest accounts cannot customize pieces.")
    else:
        while True:
            player.color = validate_color(
                ("Pick your piece color.\n"
                "Available options: "
                f"{colored('black', 'black')}, "
                f"{colored('red', 'red')}, "
                f"{colored('green', 'green')}, "
                f"{colored('yellow', 'yellow')}, "
                f"{colored('blue', 'blue')}, "
                f"{colored('magenta', 'magenta')}, "
                f"{colored('cyan', 'cyan')}, "
                f"{colored('light_grey', 'light_grey')}, "
                f"{colored('dark_grey', 'dark_grey')}, "
                f"{colored('light_red', 'light_red')}, "
                f"{colored('light_green', 'light_green')}, "
                f"{colored('light_yellow', 'light_yellow')}, "
                f"{colored('light_blue', 'light_blue')}, "
                f"{colored('light_magenta', 'light_magenta')}, "
                f"{colored('light_cyan.', 'light_cyan')}\n"
                f"{player.player_name}'s new color: ")
            )
            player.piece_type = validate_input(
                ("Pick your piece type.\n"
                "Your piece type can only contain a single uppercase (A-Z) or "
                "lowercase letter(a-z), or a single number(0-9).\n"
                "Piece Type: "),
                "^[a-zA-Z0-9]$",
                "Invalid piece type, please try again: ",
                case_sensitive = True
            )

            # Displays a preview of how their piece will be displayed on the
            # game board.
            print(f"preview: {colored(player.piece_type, player.color)}")

            piece_satisfied = validate_input(
                ("Confirm piece type and color?\n"
                "(y / n): "),
                "^(y|n)$"
            )
            clear_screen()
            if piece_satisfied == "n":
                continue
            break

        with open("users.json", "r", encoding="utf-8") as file:
            users = json.load(file)

        for user in users:
            if user["username"] == player.player_name:
                user["color"] = player.color
                user["piece_type"] = player.piece_type
                break

        with open("users.json", "w", encoding="utf-8") as file:
            json.dump(users, file, indent=4)
     
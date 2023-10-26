"""
A module containing classes that represents a User account. It is similar to
a Piece class in that they contain player information and work with
the user dictionaries in users.json, but while a Piece instance stores
attributes that defines how game pieces are represented (colors, piece types,
etc.), a User instance stores attributes that define a user's game statistics
(games played, wins, losses, etc.). It also contains functions that works with
user data.
"""


# Standard Library Modules
import json
import re
import sys

# Local Modules
from custom_errors import UsernameError


def check_json():
    """
    A function to ensure users.json exists, and that it is in the right format.
    """
    # Error handling if users.json is not found or is an invalid .json file.
    try:
        with open("users.json", "r", encoding="utf-8") as file:
            content = file.read()
            # If users.json is completely empty, make it into an empty list.
            if not content.strip():
                users = []
                with open("users.json", "w", encoding="utf-8") as file:
                    json.dump(users, file, indent=4)
            else:
                with open("users.json", "r", encoding="utf-8") as file:
                    users = json.load(file)
    # Creates users.json as an empty list if the file is missing
    except FileNotFoundError:
        with open("users.json", "w", encoding="utf-8") as file:
            json.dump([], file, indent=4)
            users = []
    except json.JSONDecodeError as error:
        # If users.json is invalid, warns user and exit.
        print(
            "JSON decoding failed. If users.json has been manually edited, "
            "there may have been an issue with the format of the file. "
            "Please backup any user data from users.json, and ensure the "
            "file is in the right format before starting the game. "
            "Exiting game now."    
        )
        print(error)
        sys.exit()
    else:
        # Warns user and exits the game if users.json exists but is not a list.
        if not isinstance(users, list):
            print(
                "Data type error. users.json should be a list. Please backup "
                "any user data from the file, and fix the issue. "
                "Exiting game now."
            )
            sys.exit()
        # Warns user and exits the game if users.json is a list but any of its
        # elements is not a dictionary. Empty lists are exempt.
        if users != []:
            for user in users:
                if not isinstance(user, dict):
                    print(
                        "Data type error. All elements in users.json should be "
                        "dictionaries. Please backup any user data from the "
                        "file, and fix the issue. Exiting game now."
                )
                    sys.exit()
    return users


def generate_users_record():
    """A function to return all of users' game records from users.json"""
    with open("users.json", "r", encoding="utf-8") as file:
        users_record = json.load(file)
    # Delete keys that has nothing to do with game history
    key_del_list = ["pin", "color", "piece_type", "logged_in"]
    for user in users_record:
        for key in key_del_list:
            del user[key]
    return users_record


def reset_log():
    """
    Function to ensure all users are logged out from the game.
    """
    with open("users.json", "r", encoding="utf-8") as file:
        users = json.load(file)
    if users != []:
        for user in users:
            user["logged_in"] = "n"
        with open("users.json", "w", encoding="utf-8") as file:
            json.dump(users, file, indent=4)


def logout(username):
    """Function for a user to log out of the game."""
    with open("users.json", "r", encoding="utf-8") as file:
        users = json.load(file)
    for user in users:
        if user["username"] == username:
            user["logged_in"] = "n"
            break
    else:
        print("Logout failed.")

    with open("users.json", "w",encoding="utf-8") as file:
        json.dump(users, file, indent=4)


class User:
    """
    Represents a user account for the game.
    
    The users contains information related to a user's game statistics, such as
    games played, wins, losses, and login status.

    Attributes:
    1. _username (str): The name of the user.
    2. _games_played (int): Total number of games played by the user.
    3. _wins (int): Total number of games won by the user.
    4. _losses (int): Total number of games lost by the user.
    5. _win_ratio (float): Games won + 1/2 games tied divided by total games
       played times 100.
    """
    def __init__(self, username, games_played, wins, losses, win_ratio):
        self._username = username
        self._games_played = games_played
        self._wins = wins
        self._losses = losses
        self._win_ratio = win_ratio

    @property
    def username(self):
        """A method to access the user's username."""
        return self._username

    @username.setter
    def username(self, username):
        """
        A method to set a user's username. It includes validation to make sure
        it is in the right format (alphanumeric, periods, and underscores only,
        5-20 characters long, name must start and end with an alphanumeric 
        character). 
        
        Raises custom UsernameError if format is not followed.  
        """
        if re.fullmatch("^[a-zA-Z0-9][a-zA-Z0-9._-]{3,18}[a-zA-Z0-9]$", username):
            self._username = username
        else:
            raise UsernameError("Invalid user name.")

    @property
    def games_played(self):
        """A method to access total number of games played by a user."""
        return int(self._games_played)

    @games_played.setter
    def games_played(self, games_played):
        """A method to set total number of games played by a user."""
        self._games_played = int(games_played)

    @property
    def wins(self):
        """A methods to access total number of games won by a user."""
        return int(self._wins)

    @wins.setter
    def wins(self, wins):
        """A method to set total number of games won by a user."""
        self._wins = int(wins)

    @property
    def losses(self):
        """A method to access total number of games lost by a user."""
        return int(self._losses)

    @losses.setter
    def losses(self, losses):
        """A method to set total number of games lost by a user."""
        self._losses = int(losses)

    @property
    def win_ratio(self):
        """A method to access win ratio of a user."""
        return round(float(self._win_ratio), 2)

    @win_ratio.setter
    def win_ratio(self, win_ratio):
        """A method to set win ratio of a user."""
        self._win_ratio = float(win_ratio)

    def update_game_history(self, winner):
        """
        A method to update the game history of a user as stored in users.json.

        Args:
        1. winner (Piece): A Piece instance that represents the player that
           won a game.
        """
        # Updates a User instance's game stats if it is not a guest account.
        if self.username.lower() != "guest":
            self.games_played += 1
            # If there is a winner, meaning the game is not a draw, wins and
            # losses are updated accordingly.
            if winner is not None:
                self.wins += 1 if winner.player_name == self.username else 0
                self.losses += 0 if winner.player_name == self.username else 1

            draws = self.games_played - (self.wins + self.losses)
            self.win_ratio = (
                ((self.wins + (0.5 * draws)) / self.games_played)
                * 100
                )
      
            # Stores updated records in users.json.
            with open("users.json", "r", encoding="utf-8") as file:
                users = json.load(file)
            for user in users:
                if user["username"] == self.username:
                    user["games_played"] = self.games_played
                    user["wins"] = self.wins
                    user["losses"] = self.losses
                    user["win_ratio"] = self.win_ratio
                    break
            with open("users.json", "w", encoding="utf-8") as file:
                json.dump(users, file, indent=4)
        else:
            pass

    def display(self):
        """Method to display own game statistics, unless user is a guest."""
        if self.username.lower() != "guest":
            print(f"{self.username}'s stats:")
            print(f"Games played: {self.games_played}")
            print(f"Wins: {self.wins}")
            print(f"Losses: {self.losses}")
            print(f"Win ratio: {self.win_ratio}%")
        else:
            print("You are using a guest account!")

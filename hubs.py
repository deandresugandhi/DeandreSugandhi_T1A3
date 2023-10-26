"""
Module that defines how hub-like instances work. It contains the parent class
of a hub-object (GameHub), and two hub-like classes inheriting attributes
and methods from GameHub itself.
"""


# Standard Library Modules
import json
import operator
import sys

# Third-party Library Modules
from termcolor import colored

#Local Modules
from utilities import change_piece_properties, clear_screen, validate_input


class GameHub:
    """
    A template to represent hub-like objects in the game. A hub is a sort of
    "lobby" where  a user can access variety of features, or move to another 
    hub. It is visualized like a room.

    Hub objects in the room will have their own specific classes, inheriting 
    and sharing attributes / methods from this class. 

    Attributes:
    1. visuals (str): The visual representation of the hub, in the form of 
       ASCII art.
    2. features (list) : A list of features available to a hub object.
    3. prompt (str): The welcome message to be displayed by the hub upon
       entering.
    """
    def __init__(
            self,
            visuals="Hub ASCII art",
            features =["list of features"],
            prompt="Type in welcome message."
    ):
        self._visuals = visuals
        self._features = features + ["exit"]
        self._prompt = prompt + "\n"

    @property
    def visuals(self):
        """A method to access the hub's visuals"""
        return self._visuals

    @property
    def features(self):
        """A method to get the hub's features"""
        return self._features

    @property
    def prompt(self):
        """A method to access the hub's welcome message"""
        return self._prompt

    def generate_feature_dict(
            self,
            feature,
            prompt,
            selections,
            function,
            additional_args = [], custom_match = None
    ):
        """
        A method to generate a feature dictionary that stores details about
        a certain feature in a hub, to be interpreted by the class methods. 
        The args represent the stored details for each feature.

        Args:
        1. feature (str): The name of the feature in the hub.
        2. prompt (str) : The welcome message displayed as a user access
           that feature.
        3. selections (list): A list of commands available for the user
           to input.
        4. function (func): The function that will be executed once the
           feature is accessed. The first arg used will be the command
           inputted by the user based on the selections list.
        5. additional_args (list): A list of additional args should a
           a function require them. Empty by default.
        6. custom_match (str): A regular expression (RegEx) formatted string
           to customize user input validation. If value is none, validation 
           is done automatically by allowing user to only input from
           selections list. Value is None by default.
        """
        feature_dict = {
            "feature": feature,
            "prompt": prompt,
            "selections": selections,
            "function": function,
            "additional_args": additional_args,
            "custom_match": custom_match,
        }
        return feature_dict

    def access_hub(self):
        """
        A method that defines what happens when a user enters a hub.
        
        Returns user command based on their input
        """
        # Generates regex for input validation, based on self.features.
        match = f"^({'|'.join(self.features)})$"
        # Generates text to let users know what commands are accepted,
        # i.e. the features available in the hub.
        command_list = f"({' / '.join(self.features)}): "
        new_prompt = self.prompt + command_list
        # Displays the hub's ASCII art.
        print(self.visuals)
        # Validates user command. Loops until input command is valid.
        command = validate_input(new_prompt, match)
        return command

    def move_hub(self, move_to):
        """
        A method that is called when a user wants to move from one hub to
        another.

        Args:
        1. move_to (str): The name of the hub to move into.

        Returns the name of the hub to move into.
        """
        return move_to

    def access_feature(self, feature_dict):
        """
        A method that is called when a user wants to access a feature in the
        hub.

        Args:
        1. feature_dict (dict): A dictionary detailing a feature's details.
           Generated by self.generate_feature_dict().

        Returns False if the user wants to exit the feature, or the name of the
        new hub to move into if the user calls self.move_hub().
        """
        # Generates regex to validate user input, based on the selections key
        # in the dictionary. If custom_match key has a set value, it will use
        # this value instead (a regex string) to validate the input.
        match = (f"^({'|'.join(feature_dict.get('selections'))})$"
                if feature_dict.get('custom_match') is None
                else feature_dict.get('custom_match'))
        # Generates text to let users know what commands are accepted.
        command_list = f"({' / '.join(feature_dict.get('selections'))}): "
        new_prompt = feature_dict.get('prompt') + "\n" + command_list

        # Loops as long as the user is still accessing the feature, i.e. user
        # has not called exit.
        while True:
            # Validates user command. Loops until input command is valid.
            command = validate_input(new_prompt, match)

            if command.lower() == "exit":
                return False

            # If command is a move_hub() function, return the new hub.
            # Else, perform the function, with additional args as specified by
            # the feature dictionary.
            function_args = feature_dict.get("additional_args", [])
            if feature_dict.get("function") != self.move_hub:
                feature_dict.get("function")(command, *function_args)
            else:
                return feature_dict.get("function")(*function_args)

    def enter_logic(self, features_list):
        """
        A method that defines how the whole experience of entering a hub,
        accessing its features, and leaving it, works. It combines all the
        other class methods,

        Args:
        1. features_list (list): A list of feature dictionaries.

        Returns exit if the user wants to exit the hub, or if the user wants
        to move to another hub, return the name of the new hub. 
        """
        # Loops as long as the user is still in the hub, i.e. haven't exited
        # or moved to another hub.
        while True:
            # Enters hub. Return user command.
            command = self.access_hub()
            # If command is not exit, user wants to access a feature.
            if command.lower() != "exit":
                # Finds the feature in features_list that matches user command.
                for feature_dict in features_list:
                    if feature_dict.get("feature") == command.lower():
                        # Access the feature. Returns a value once the user
                        # is done with a feature.
                        move_to = self.access_feature(feature_dict)
                        # If the user exits the feature, False is returned, and
                        # loop breaks. User goes back to the hub.
                        if move_to is False:
                            break
                        # If the user exits a feature by moving to another
                        # hub, returns the name of the new hub.
                        return move_to
            # If command is exit, verify if the user really wants to exit. If
            # so, "exit" is returned.
            else:
                confirm_exit = validate_input("Confirm exit (y / n): ", "^(y|n)$")
                if confirm_exit == "n":
                    continue
                return "exit"


class PlayerLounge(GameHub):
    """
    Represents the lounge of the game, a hub with features such as piece 
    customization, high-score board, and search for a specific user's record.

    The class inherits from the GameHub class which represents hub-like objects.

    Attributes:
    1. customi - u2 (str): Colored string to be displayed in the hub's ASCII art.
    2. users_record (list) = List of dictionaries, each dictionary containing
       a user's game history.
    """
    def __init__(self, users_record):
        customi = colored("CUSTOMIZE", "cyan")
        high_sco = colored("HIGH SCORE", "yellow")
        ex_to = colored("EXIT TO", "red")
        lob = colored("LOBBY", "red")
        u1 = colored("USER", "magenta")
        u2 = colored("INFO", "magenta")
        super().__init__(
            visuals=fr"""
  \_                                                      _/
    \_                                                  _/
      \                                                /
       |                                              |
       |_________                            _________|
       |         |\ ______________________ /|         |      
       |         | |      __________      | |         |
       |         | |     |{high_sco}|     | | {ex_to} |
       |{customi}| |____ | *....... |     | |  {lob}  |
       | <------ |/____/|| *....... |     | | ------> |       
       |         ||{u1}|||__________|     | |         |
       |         ||{u2}||_________________| |         |
       |_________||____|/                  \|_________|
       |                                              |
       |                                              |
     _/                                                \_
    /                                                    \
            """,
            features=["customize", "user_info", "high_score"],
            prompt=(
                "Welcome to the player lounge! Here you can customize" 
                "your piece and access player statistics." 
            )
        )
        self._users_record = users_record


    @property
    def users_record(self):
        """A method to access the users record."""
        return self._users_record

    @users_record.setter
    def users_record(self, users_record):
        """A method to set the users record."""
        self._users_record = users_record

    @property
    def visuals(self):
        """A method to access the hub's ASCII art representation."""
        return self._visuals

    def update_users_record(self):
        """A method to update the ._users_record attribute."""
        with open("users.json", "r", encoding="utf-8") as file:
            users_record = json.load(file)
        key_del_list = ["pin", "color", "piece_type", "logged_in"]
        for user in users_record:
            for key in key_del_list:
                del user[key]
        self.users_record = users_record

    def display_user_details(self, username):
        """
        A method to display a user detail (dictionary) in self.users_record.
        
        Args:
        1. username = The username key that will be searched in self.users_record
           and displayed along with the rest of the user details (dictionary).
        """
        for user in self.users_record:
            if user["username"] == username:
                print(f"{user['username']}'s stats:")
                print(f"Games played: {user['games_played']}")
                print(f"Wins: {user['wins']}")
                print(f"Losses: {user['losses']}")
                print(f"Win ratio: {user['win_ratio']}%")
                break
        else:
            print("Invalid username.")

    def display_high_scorer(self, sorter):
        """
        A method to display the 5 highest scorers along with their respective
        user details based on a given sorter.

        Args:
        1. sorter (str): Determines the criteria from which to display the
           highest scorers (e.g. "wins", "games played," "win_ratio", etc.).
        """
        sorted_list = sorted(
            self.users_record,
            key=operator.itemgetter(sorter),
            reverse=True
        )

        print(f"Most {sorter}:\n")

        count = 0
        for user in sorted_list:
            print(f"{user['username']}'s stats:")
            print(f"Games played: {user['games_played']}")
            print(f"Wins: {user['wins']}")
            print(f"Losses: {user['losses']}")
            print(f"Win ratio: {user['win_ratio']}%\n\n\n")
            count += 1
            # Display 5 records. Or if there are fewer than 5 records in
            # users record, display all.
            if count == 5 or count == len(self.users_record):
                break

    def customization(self, command, players):
        """
        A method to access the piece customization feature of the PlayerLounge
        hub. 

        Args:
        1. command (str): The command entered by the user, representing the
           player that wants to customize their piece (i.e. "p1" and "p2").
        2. players (list): A list of Piece instances of the game players.
        """
        if command.lower() == "p1":
            clear_screen()
            change_piece_properties(players[0])
        elif command.lower() == "p2":
            clear_screen()
            change_piece_properties(players[1])
        else:
            raise ValueError("Unknown command. Please try again: ")

    def enter(self, players):
        """
        A method that defines what happens when a player decide to enter the
        PlayerLounge hub. This method uses inherited methods from the
        GameHub class.


        Args:
        1. players (list): A list of Piece instances of the game players
           entering the lounge.
        """
        # Ensures users record is up to date.
        self.update_users_record()

        # Create a dictionary for each feature of the lounge. It details the
        # feature name, the prompt that will be asked, the selections of
        # commands available for user input, and the function that will be
        # executed when the feature is accessed.
        customize_dict = self.generate_feature_dict(
            self.features[0],
            "Which player is customizing?",
            ["p1", "p2", "exit"],
            self.customization,
            # Extra arg for the self.customization method
            [players],
        )
        user_info_dict = self.generate_feature_dict(
            self.features[1],
            "Which user do you want to view?",
            ["Type username", "exit"],
            self.display_user_details,
            # Disables validation and lets user type in unrestricted lines
            # of string as a keyword for username search.
            custom_match=".*"
        )
        high_score_dict = self.generate_feature_dict(
            self.features[2],
            "Which high-score board do you want to view?",
            ["wins", "games_played", "win_ratio", "exit"],
            self.display_high_scorer,
        )

        features_list = [customize_dict, user_info_dict, high_score_dict]

        # self.enter_logic defines what happens when the user enters the hub,
        # and returns where the user wants to go next once they decide to leave
        # the lounge, stored in new_hub variable.
        new_hub = self.enter_logic(features_list)
        # Defines the behavior of the "exit" command
        if new_hub == "exit":
            return "lobby"
        else:
            # Move to the new hub
            return new_hub


class MainLobby(GameHub):
    """
    Represents the main lobby of the game, which is the landing area after the
    players have logged in. It is the hub from which the players can access the
    main matchmaking system and the player lounge.

    The class inherits from the GameHub class which represents hub-like objects.

    Attributes:
    1. loun - ex (str): Colored strings to be displayed in the hub's ASCII art.
    """
    def __init__(self):
        loun = colored("LOUNGE", "blue")
        mat = colored("MATCH", "green")
        ex = colored("EXIT", "red")
        super().__init__(
            visuals=fr"""
   \_                                             _/
     \_                                         _/
       \                                       /
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
        |                 / \                 |
      _/                 / | \                 \_
     /                     |                     \
                           |                               
            """,
            features = ["lounge", "match"],
            prompt=(
                "Welcome to Terminal Connect Four! Select an option:\n"
                "LOUNGE: Customize your piece, or view player statistics\n"
                "MATCH: Start a player match\n"
                "EXIT: All users logout and exit the game"
            )
        )

    @property
    def visuals(self):
        """A method to access the hub's ASCII art representation."""
        return self._visuals

    def enter(self):
        """
        A method that defines what happens when a player decide to enter the
        MainLobby hub. This method uses inherited methods from the
        GameHub class.
        """
        # Create a dictionary for each feature of the main lobby. It details the
        # feature name, the prompt that will be asked, the selections of
        # commands available for user input, and the function that will be
        # executed when the feature is accessed.
        lounge_dict = self.generate_feature_dict(
            self.features[0],
            "Enter the lounge?",
            ["press Enter", "exit"],
            self.move_hub,
            ["lounge"],
            # Disables validation and lets user type in unrestricted lines
            # of string because entering does not require a specific format.
            custom_match=".*"
        )

        match_dict = self.generate_feature_dict(
            self.features[1],
            "Start a match?",
            ["press Enter", "exit"],
            self.move_hub,
            ["match"],
            # Disables validation and lets user type in unrestricted lines
            # of string because entering does not require a specific format.
            custom_match=".*"
        )

        features_list = [lounge_dict, match_dict]
        # self.enter_logic defines what happens when the user enters the hub,
        # and returns where the user wants to go next once they decide to leave
        # the lounge, stored in new_hub variable.
        move_to = self.enter_logic(features_list)
        # Defines the behavior of the "exit" command
        if move_to == "exit":
            sys.exit()
        else:
            # Move to the new hub.
            return move_to

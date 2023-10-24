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


class GameHub:
    def __init__(self, visuals="Hub ASCII art", features = ["features"], prompt="Type in welcome message."):
        self._visuals = visuals
        self._features = features + ["exit"]
        self._prompt = prompt + "\n"
    
    @property
    def visuals(self):
        return self._visuals
    
    @property
    def features(self):
        return self._features
    
    @property
    def prompt(self):
        return self._prompt
    
    def generate_feature_dict(self, feature, prompt, selections, function, additional_args = [], custom_match = None):
            dict = {
                "feature": feature,
                "prompt": prompt,
                "selections": selections,
                "function": function,
                "additional_args": additional_args,
                "custom_match": custom_match,
            }
            return dict

    def access_hub(self):
        match = f"^({'|'.join(self.features)})$"
        command_list = f"({' / '.join(self.features)}): "
        new_prompt = self.prompt + command_list
        print(self.visuals)
        command = validate_input(new_prompt, match)
        return command
    
    def move_hub(self, move_to):
        return move_to

    def access_feature(self, feature_dict):
        match = f"^({'|'.join(feature_dict.get('selections'))})$" if feature_dict.get('custom_match') == None else feature_dict.get('custom_match') 
        command_list = f"({' / '.join(feature_dict.get('selections'))}): "
        new_prompt = feature_dict.get('prompt') + "\n" + command_list
        while True:
            command = validate_input(new_prompt, match)
            if command.lower() == "exit":
                return False
            else:
                function_args = feature_dict.get("additional_args", [])
                if feature_dict.get("function") != self.move_hub:
                    feature_dict.get("function")(command, *function_args)
                else:
                    return feature_dict.get("function")(*function_args)
    
    def enter_logic(self, features_list):
        while True:
            command = self.access_hub()
            if command.lower() != "exit":
                for feature_dict in features_list:
                    if feature_dict.get("feature") == command.lower():
                        move_to = self.access_feature(feature_dict)
                        if move_to == False:
                            break
                        else:
                            return move_to
            else:
                confirm_exit = validate_input("Confirm exit (y / n): ", "^(y|n)$")
                if confirm_exit == "n":
                    continue
                return "exit"
            
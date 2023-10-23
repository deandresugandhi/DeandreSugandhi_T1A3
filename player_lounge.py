import json
import operator
from utilities import validate_input
from termcolor import colored

def generate_users_record():
    with open("users.json", "r") as file:
        users_record = json.load(file)
    key_del_list = ["pin", "color", "piece_type", "logged_in"]
    for user in users_record:
        for key in key_del_list:
            del user[key]
    return users_record

class PlayerLounge:
    def __init__(self, users_record):
        customi = colored("CUSTOMIZE", "cyan")
        high_sco = colored("HIGH-SCORE", "yellow")
        ex = colored("EXIT", "red")
        self._users_record = users_record
        self._lounge = fr"""
          \_                                                    _/
            \_                                                _/
              \                                          ____/
               |                                        |
               |_________                      _________|
               |         |\ ________________ /|         |      
               |         | |   __________   | |         |
               |         | |  |{high_sco}|  | |         |
               |{customi}| |  | *....... |  | |  {ex}   |
               | <------ | |  | *....... |  | | ------> |       
               |         | |  |__________|  | |         |
               |         | |________________| |         |
               |_________|/                  \|_________|
               |                                        |
           ____|                                        |___
         _/                                                 \_
        /                                                     \
        """

    @property
    def users_record(self):
        return self._users_record

    @property
    def lounge(self):
        return self._lounge
    
    def access_user_details(self, username):
        for user in self.users_record:
            if user["username"] == username:
                print(f"{user['username']}'s stats:")
                print(f"Games played: {user['games_played']}")
                print(f"Wins: {user['wins']}")
                print(f"Losses: {user['losses']}")
                print(f"Win ratio: {user['win_ratio']}")
        else:
            raise ValueError("Invalid username. Please try again: ")
    
    def display_high_scorer(self, sorter):
        sorted_list = sorted(self.users_record, key=operator.itemgetter(sorter), reverse=True)
        print(f"Most {sorter}: ")
        count = 0
        for user in sorted_list:
            print(f"{user['username']}'s stats:")
            print(f"Games played: {user['games_played']}")
            print(f"Wins: {user['wins']}")
            print(f"Losses: {user['losses']}")
            print(f"Win ratio: {user['win_ratio']}\n\n\n")
            count += 1
            if count == 5 or count == len(self.users_record):
                break
    
    def enter_lounge(self):
        while True:
            print(self.lounge)
            command = validate_input(
                ("Welcome to the player lounge! Here you can customize your piece and access player statistics.\n"
                "(high_score / customize / player_info / exit): "),
                "^(high_score|customize|player_info|exit)$"
            )
            match command:
                case "high_score":
                    command = validate_input(
                        ("Which high-score board do you want to view?\n"
                        "(wins / games_played / win_ratio / exit): "),
                        "^(wins|games_played|win_ratio|exit)$"
                    )
                    if command.lower() != "exit":
                        self.display_high_scorer(command)
                    else:
                    

            case "customize":

            case "player_info":
                
            case "exit":
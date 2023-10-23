import json
import operator
from utilities import validate_input

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
        self._users_record = users_record
        self._lounge = r"""
  \_                                                    _/
    \_                                                _/
      \                                          ____/
       |                                        |
       |_________                      _________|
       |         |\ ________________ /|         |      
       |         | |   __________   | |         |
       |         | |  |HIGH-SCORE|  | |         |
       |CUSTOMIZE| |  | *....... |  | |  EXIT   |
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
    
    def display_lounge(self):
        print(self.lounge)
        command = validate_input(
            "Welcome to the player lounge! Here you can customize your piece and access player information.\n"
            "Please enter a command: ",
            "^(high-score|customize|player-info|exit)$"
        )
        return command.lower()

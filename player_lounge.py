import json
import operator
from utilities import validate_input, update_attributes, change_piece_properties, clear_screen, GameHub
from termcolor import colored

def generate_users_record():
    with open("users.json", "r") as file:
        users_record = json.load(file)
    key_del_list = ["pin", "color", "piece_type", "logged_in"]
    for user in users_record:
        for key in key_del_list:
            del user[key]
    return users_record

class PlayerLounge(GameHub):
    def __init__(self, users_record):
        customi = colored("CUSTOMIZE", "cyan")
        high_sco = colored("HIGH_SCORE", "yellow")
        ex = colored("EXIT", "red")
        u1 = colored("USER", "magenta")
        u2 = colored("INFO", "blue")
        super().__init__(
            visuals=fr"""
  \_                                                      _/
    \_                                                  _/
      \                                                /
       |                                              |
       |_________                            _________|
       |         |\ ______________________ /|         |      
       |         | |      __________      | |         |
       |         | |     |{high_sco}|     | |         |
       |{customi}| |____ | *....... |     | |  {ex}   |
       | <------ |/____/|| *....... |     | | ------> |       
       |         ||{u1}|||__________|     | |         |
       |         ||{u2}||_________________| |         |
       |_________||____|/                  \|_________|
       |                                              |
       |                                              |
     _/                                                \_
    /                                                    \
            """,
            features=["high_score", "customize"],
            prompt="Welcome to the player lounge! Here you can customize your piece and access player statistics." 
        )
        self._users_record = users_record
      

    @property
    def users_record(self):
        return self._users_record

    @property
    def visuals(self):
        return self._visuals
    
    def update_users_record(self):
        with open("users.json", "r") as file:
            users_record = json.load(file)
        key_del_list = ["pin", "color", "piece_type", "logged_in"]
        for user in users_record:
            for key in key_del_list:
                del user[key]
        self.users_record = users_record 

    def display_user_details(self, username):
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
    
    def customization(self, command, players):
        if command.lower() == "p1":
            clear_screen()
            change_piece_properties(players[0])
        elif command.lower() == "p2":
            clear_screen()
            change_piece_properties(players[1])
        else:
            raise ValueError("Unknown command. Please try again: ")
        
    def enter(self, players):
        high_score_dict = self.generate_feature_dict(
            self.features[0],
            "Which high-score board do you want to view?",
            ["wins", "games_played", "win_ratio", "exit"],
            self.display_high_scorer,
            []
        )

        customize_dict = self.generate_feature_dict(
            self.features[1],
            "Which player is customizing?",
            ["p1", "p2", "exit"],
            self.customization,
            [players],
        )

        features_list = [high_score_dict, customize_dict]

        self.enter_logic(features_list)
        return "back_to_lobby"

        


import json
import re
import atexit
from utilities import clear_screen

def reset_login():
    with open("users.json", "r") as file:
        users = json.load(file)
    if users != []:
        for user in users:
            user["logged_in"] = "n"
        with open("users.json", "w") as file:
            json.dump(users, file, indent=4)

def logout(username):
    with open("users.json", "r") as file:
        users = json.load(file)
    for user in users:
        if user["username"] == username:
            user["logged_in"] = "n"
            break
    else:
        print("Logout failed.")

    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)

class User:
    def __init__(self, username, games_played, wins, losses, win_ratio):
        self._username = username
        self._games_played = games_played
        self._wins = wins
        self._losses = losses
        self._win_ratio = win_ratio

    @property
    def username(self):
        return self._username
    
    @username.setter
    def username(self, username):
        if re.fullmatch("^[a-zA-Z0-9][a-zA-Z0-9._-]{3,18}[a-zA-Z0-9]$", username):
            self._username = username
        else:
            raise ValueError("Invalid name.")
        
    @property
    def games_played(self):
        return int(self._games_played)
    
    @games_played.setter
    def games_played(self, games_played):
        self._games_played = int(games_played)

    @property
    def wins(self):
        return int(self._wins)
    
    @wins.setter
    def wins(self, wins):
        self._wins = int(wins)
    
    @property
    def losses(self):
        return int(self._losses)
    
    @losses.setter
    def losses(self, losses):
        self._losses = int(losses)

    @property
    def win_ratio(self):
        return round(float(self._win_ratio), 1)
    
    @win_ratio.setter
    def win_ratio(self, win_ratio):
        self._win_ratio = float(win_ratio)
        
    def update_game_history(self, winner):
        if self.username.lower() != "guest":
            self.games_played += 1
            self.wins += 1 if winner.player_name == self.username else 0
            self.losses += 0 if winner == None else 1
            self.win_ratio = self.wins / self.losses

            with open("users.json", "r") as file:
                users = json.load(file)

            for user in users:
                if user["username"] == self.username:
                    user["games_played"] = self.games_played
                    user["wins"] = self.wins
                    user["losses"] = self.losses
                    user["win_ratio"] = self.win_ratio
                    break

            with open("users.json", "w") as file:
                json.dump(users, file, indent=4)
        else:
            pass

    def display(self):
        if self.username.lower() != "guest":
            print(f"{self.username}'s stats:")
            print(f"Games played: {self.games_played}")
            print(f"Wins: {self.wins}")
            print(f"Losses: {self.losses}")
            print(f"Win ratio: {self.win_ratio}")
        else:
            print("You are using a guest account!")


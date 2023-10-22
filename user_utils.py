import json
import atexit

def reset_login():
    with open("users.json", "r") as file:
        users = json.load(file)
    for user in users:
        user["logged_in"] = "n"
    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)

def logout(user):
    with open("users.json", "r") as file:
        users = json.load(file)
    for user in users:
        if user["logged_in"] == "y":
            user["logged_in"] = "n"
    with open("users.json", "w") as file:
        json.dump(users, file, indent=4)


class User:
    def __init__(self, username, games_played, wins, losses, win_ratio):
        self._username = username
        self._games_played = games_played
        self._wins = wins
        self._losses = losses
        self._win_ratio = win_ratio
    
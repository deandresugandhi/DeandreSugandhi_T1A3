import re


def game_setup(player):
    player_status = input(f"Player {player.player}! Are you a new or existing user? (new / existing)")
    if player_status == "new":
        account_type = input("Do you want to create your own account or use a guest account?\n"
                            "Note: Create an account if you want to be recorded in the high-score board, "
                            "have access to your own game stats, and have more customization for your piece. \n" 
                            "(own / guest): ")
        if account_type == "own":
            username = input("Please create a username for your account. This will also be your display name. \n"
                            "1. Usernames can only contain uppercase (A-Z) or lowercase "
                            "letters (a-z), numbers(0-9), periods (.), and underscores (_).\n"
                            "2. Usernames cannot start or end with a period(.) or underscore(.).\n"
                            "3. Usernames should be between 5 - 20 characters long.\n"
                            "Username: ")
            pin = input("Please enter a 4-digit PIN for your account. This will be used to verify your future sign-ins. \n"
                        "PIN: ")
            print("Your account has been created!")
            player.color = input("Pick your piece color.\n"
                                 "Available options: black, red, green, yellow, blue, magenta, cyan, white, light_grey, "
                                 "dark_grey, light_red, light_green, light_yellow, light_blue, light_magenta, light_cyan"
                                 "Color: ").lower()
            player.piece_type = input("Pick your piece type")
    
    
    elif player_status == "existing":
    player1.color = input("Pick your piece color")


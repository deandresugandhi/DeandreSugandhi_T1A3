import re

def validate_input(prompt):
    while True:
        try:
            input(prompt)
        except ValueError as error_message:
            print(error_message)

        
def game_setup(player):
    player_status = validate_input(f"Player {player.player}! Are you a new or existing user? (new / existing)")
    if player_status == "new":
        account_type = validate_input("Do you want to create your own account or use a guest account?\n"
                            "Note: Create an account if you want to be recorded in the high-score board, "
                            "have access to your own game stats, and have more customization for your piece. \n" 
                            "(own / guest): ")
        if account_type == "own":
            username = validate_input("Please create a username for your account. This will also be your display name. \n"
                            "1. Usernames can only contain uppercase (A-Z) or lowercase "
                            "letters (a-z), numbers(0-9), periods (.), and underscores (_).\n"
                            "2. Usernames cannot start or end with a period(.) or underscore(.).\n"
                            "3. Usernames should be between 5 - 20 characters long.\n"
                            "Username: ")
            pin = validate_input("Please enter a 4-digit PIN for your account. This will be used to verify your future sign-ins. \n"
                        "PIN: ")
            print("Your account has been created!")
            player.color = validate_input("Pick your piece color.\n"
                                 "Your piece color determines the color of your piece on the board."
                                 "Available options: black, red, green, yellow, blue, magenta, cyan, white, light_grey, "
                                 "dark_grey, light_red, light_green, light_yellow, light_blue, light_magenta, light_cyan"
                                 "Color: ").lower()
            player.piece_type = validate_input("Pick your piece type.\n"
                                      "Your piece type determines the form that represents your piece on the board."
                                      "It can only contain a single uppercase (A-Z) or lowercase letter(a-z), or a single number(0-9).")
    
    elif player_status == "existing":
        player.color = validate_input("Pick your piece color")


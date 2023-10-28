"""
Module to define how a Connect Four match is run. 

Includes four functions that represents the three phases of the game:
1. game_start(): Pre-game
1. game_in_progress(): From start of game to when a win / loss / draw is 
   detected
2. game_complete(): From end of game to decision on what to do post-game
3. game_reset(): When players want to play again
"""


# Standard Library Modules
import re

# Third Party Modules
from termcolor import colored

# Local Modules
from custom_errors import ColumnFullError
from utilities import (
    clear_screen,
    reset_screen,
    validate_input,
    change_piece_properties
)

def game_start(players):
    """
    Function to validate the pre-conditions before a game can start.

    Args:
    1. players (list): A list of Piece instances, defining the players
       playing the game.
    """

    def ask_to_change_piece_properties(player):
        """
        Function to validate input to change the piece properties of a player.
        
        Args:
        1. player(Piece): A Piece instance of the player to be modified.
        """
        player_changing = validate_input(
            (f"Does {player.player_name} want to change piece properties?\n"
            "(y / n): "),
            "^(y|n)$"
        )
        if player_changing == "y":
            change_piece_properties(player)
        else:
            pass

    clear_screen()

    # Change properties of the players' pieces until they don't have the exact
    # visual representation of their pieces (both color and type).
    while (
        players[0].color == players[1].color and
        players[0].piece_type == players[1].piece_type
    ):
        print(
            "In order to start the game, both players cannot have the "
            "exact same piece type and color. Please change "
            "piece type / color accordingly.")
        ask_to_change_piece_properties(players[0])
        ask_to_change_piece_properties(players[1])

    input(f"{colored(players[0].player_name, players[0].color)} and "
          f"{colored(players[1].player_name, players[1].color)}, "
          "press enter when ready! ")


def game_in_progress(board, players, referee):
    """
    Function to decide how a game is run from start until when game result is
    detected.
    
    Args:
    1. board (Board): An instance of the Board class, defining the board in
       which the game will be played.
    2. players (Piece): An instance of the Piece class, defining the players
       playing the game.
    3. referee (VictoryChecker): An instance of the VictoryChecker class,
       defining the referee that checks the state of the board each game turn
       to see if the game should be over.
    """
    player_turn = 0
    move_count = 0

    # Game loops as long as referee does not detect a winner and there are
    # less than 42 move counts, which is the total number of slots available in
    # the board.
    while referee.check_victory() is None and move_count < 42:
        # Refreshes the screen and board state
        reset_screen(board)

        player_command = input(
            f"\n{colored(players[player_turn].player_name, players[player_turn].color)}"
            f"'s turn: "
        )

        # Input loops until the player makes a valid move"
        while True:
            if re.fullmatch("^([1-7]|clear|surrender)$", player_command.lower()):
                # If it's a digit between 1-7, within game columns limit,
                # drop is attempted
                if player_command.isdigit():
                    try:
                        players[player_turn].drop(board, int(player_command))
                    # If column is full, piece drop and input is refused.
                    except ColumnFullError as error:
                        player_command = input(error)
                    # If piece drop is successful, alternate player turn and
                    # increase move count by 1.
                    else:
                        player_turn = int(not player_turn)
                        move_count += 1
                        break
                # If "clear", game is reset. No wins are recorded.
                elif player_command.lower() == "clear":
                    board.clear_board()
                    player_turn = 0
                    move_count = 0
                    break
                # If "surrender", the player's surrender state is turned on,
                # and the player loses the game.
                elif player_command.lower() == "surrender":
                    players[player_turn].surrender = True
                    reset_screen(board)
                    # Returns the winning Piece and the surrendering Piece.
                    return referee.check_victory(), players[player_turn]
            else:
                player_command = input("Invalid input, please try again: ")

    reset_screen(board)
    # Returns referee's result (None if no winners hence draw), and surrendering
    # Piece (which is None) as a tuple.
    return referee.check_victory(), None


def game_complete(game_result, users):
    """
    Function to decide what is to be done when game is completed. Users' stats
    in the .json file are updated.
    
    Args:
    1. game_result (tuple): A tuple containing the names of the winning player
       (if any) & surrendering player (if any). Returned by game_in_progress().
    2. users (list): A list of User instances to update game stats.
    """
    winner, surrendered = game_result
    if winner is None:
        print("Game Draw!")
    else:
        if surrendered is not None:
            print(f"{surrendered.player_name} surrendered!")
        print(f"{winner.player_name} wins!")

    # Updates each user's game stats
    users[0].update_game_history(winner)
    users[1].update_game_history(winner)

    play_again = validate_input("Play again? (y / n): ","^[yn]$")
    return play_again


def game_reset(board, players):
    """
    Function to reset the board and set each player's surrender state to False
    when players want to rematch.

    Args:
    1. board (Board): An instance of the Board class, representing the board in
       which the game will be played. 
    2. players (list): A list of Piece instances of the game players.
    """
    board.clear_board()
    players[0].surrender = False
    players[1].surrender = False

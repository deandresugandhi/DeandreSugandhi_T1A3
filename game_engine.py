from utilities import clear_screen, reset_screen, validate_input


def game_in_progress(board, players, referee):
    player_turn = 0
    move_count = 0

    while referee.check_victory() is None and move_count < 42:
        reset_screen(board)
        player_command = input(f"{players[player_turn]._player_name}'s turn: ")
        if player_command.lower() == "clear":
            board.clear_board()
            player_turn = 0
            continue
        elif player_command.lower() == "surrender":
            players[player_turn].surrender = True
            reset_screen(board)
            return referee.check_victory(), players[player_turn]
        players[player_turn].drop(board, int(player_command))
        player_turn = int(not player_turn)
        move_count += 1
        continue
    reset_screen(board)
    return referee.check_victory(), None


def game_complete(game_result, users):
    winner, surrendered = game_result
    if winner is None:
        print("Game Draw!")
    else:
        if surrendered is not None:
            print(f"{surrendered.player_name} surrendered!") 
        print(f"{winner.player_name} wins!")
        
    users[0].update_game_history(winner)
    users[1].update_game_history(winner)

    play_again = validate_input("Play again? (y / n): ","^[yn]$")
    return play_again

def game_reset(board, players):
    board.clear_board()
    players[0].surrender = False
    players[1].surrender = False

    

    




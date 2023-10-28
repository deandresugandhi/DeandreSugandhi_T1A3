"""
Module to test important methods from hubs.py
"""


import pytest
from hubs import PlayerLounge, MainLobby
from game_board import Piece
from user_utils import generate_users_record


def test_player_lounge_enter_check_high_score_exit(monkeypatch):
    """
    Tests the following sequence: enter player lounge, checks high score board,
    sorts high score with "games_played" keyword, exits high score board, and 
    exits player lounge.
    """
    # Define required variables
    player1 = Piece("Test1","red", "O", 1)
    player2 = Piece("Test2","blue", "X", 2)
    players = [player1, player2]
    users_record = generate_users_record()
    lounge = PlayerLounge(users_record)

    # Print commands that will be captured
    captured_print = []
    # Expected print commands if test is successful
    expected_print = [
        "Most games_played:\n",
        "tester123's stats:",
        "Games played: 5",
        "Wins: 2",
        "Losses: 1",
        "Win ratio: 60.0%\n\n\n",
        "tester321's stats:",
        "Games played: 2",
        "Wins: 1",
        "Losses: 0",
        "Win ratio: 75.0%\n\n\n",
        "tester009's stats:",
        "Games played: 0",
        "Wins: 0",
        "Losses: 0",
        "Win ratio: 0.0%\n\n\n"
    ]

    # Sequence of user input to achieve the desired sequence of commands
    input_sequence = iter([" ", "high_score", "games_played", "exit", "exit", "y"])

    # Mock print function to catch print commands and append to
    # captured_print
    def mock_print(*args):
        output = " ".join(map(str, args))
        captured_print.append(output)

    # Replaces default print function to mock_print
    monkeypatch.setattr("builtins.print", mock_print)
    # Replaces default input function to enter input_sequence in sequence
    monkeypatch.setattr("builtins.input", lambda _: next(input_sequence))

    # Main function
    result = lounge.enter(players)

    # Function should return and print the following
    assert result == "lobby"
    assert captured_print[1:-1] == expected_print


def test_player_lounge_enter_check_user_info_exit(monkeypatch):
    """
    Tests the following sequence: enter player lounge, checks user info,
    type in "tester123" as username, exits user info, and exits player lounge.
    """
    # Define required variables
    player1 = Piece("Test1","red", "O", 1)
    player2 = Piece("Test2","blue", "X", 2)
    players = [player1, player2]
    users_record = generate_users_record()
    lounge = PlayerLounge(users_record)

    # Print commands that will be captured
    captured_print = []
    # Expected print commands if test is successful
    expected_print = [
        "tester123's stats:",
        "Games played: 5",
        "Wins: 2",
        "Losses: 1",
        "Win ratio: 60.0%",
    ]

    # Sequence of user input to achieve the desired sequence of commands
    input_sequence = iter([" ", "user_info", "tester123", "exit", "exit", "y"])

    # Mock print function to catch print commands and append to
    # captured_print
    def mock_print(*args):
        output = " ".join(map(str, args))
        captured_print.append(output)

    # Replaces default print function to mock_print
    monkeypatch.setattr("builtins.print", mock_print)
    # Replaces default input function to enter input_sequence in sequence
    monkeypatch.setattr("builtins.input", lambda _: next(input_sequence))

    # Main function
    result = lounge.enter(players)

    # Function should return and print the following
    assert result == "lobby"
    assert captured_print[1:-1] == expected_print


def test_main_lobby_to_lounge(monkeypatch):
    """
    Tests the following sequence: enter main lobby, enter player lounge from
    main lobby.
    """
    # Define required variables
    lobby = MainLobby()

    # Sequence of user input to achieve the desired sequence of commands
    input_sequence = iter(["lounge", " "])

    # Replaces default input function to enter input_sequence in sequence
    monkeypatch.setattr("builtins.input", lambda _: next(input_sequence))

    # Main function
    result = lobby.enter()

    # Function should return the following:
    assert result == "lounge"


def test_main_lobby_exit(monkeypatch):
    """
    Tests the following sequence: enter main lobby, exit main lobby (exit
    the game)
    """
    # Define requried variables
    lobby = MainLobby()

    # Sequence of user input to achieve the desired sequence of commands
    input_sequence = iter(["exit", "y"])

    # Mock_exit function to raise SystemExit()
    def mock_exit():
        raise SystemExit()

    # Replaces sys.exit with mock_exit, raising SystemExit() instead
    monkeypatch.setattr("builtins.input", lambda _: next(input_sequence))
    # Replaces default input function to enter input_sequence in sequence
    monkeypatch.setattr("sys.exit", mock_exit)

    with pytest.raises(SystemExit) as exception:
        lobby.enter()

    # SystemExit should be raised if sys.exit is called by exiting the lobby
    assert exception.type == SystemExit
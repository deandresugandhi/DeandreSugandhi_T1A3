"""
Module to test important functions from game_engine.py
"""


import pytest
from game_engine import game_in_progress
from game_board import Board, Piece
from win_conditions import VictoryChecker


def test_game_in_progress_p1wins_vertical_victory(monkeypatch):
    """
    Tests the following sequence during game_in_progress: player 1 putting
    pieces in column 1 during their turn and player 2 putting pieces in column
    2 during their turn. This should result in player 1 vertical victory.
    """
    # Define required variables
    player1 = Piece("Test1","red", "O", 1)
    player2 = Piece("Test2","blue", "X", 2)
    players = [player1, player2]
    board = Board(players)
    referee = VictoryChecker(board, players)

    # Sequence of user input to achieve the desired sequence of commands
    input_sequence = iter(["1", "2", "1", "2","1", "2", "1"])

    # Replaces default input function to enter input_sequence in sequence
    monkeypatch.setattr("builtins.input", lambda _: next(input_sequence))
    
    # Main function
    result = game_in_progress(board, players, referee)

    # Function should return player 1 as a winner, with no surrendered players
    assert result == (player1, None)


def test_game_in_progress_p1wins_horizontal_victory(monkeypatch):
    """
    Tests the following sequence during game_in_progress: players 1 and 2
    putting their pieces on columns 1 - 4 alternatingly. This should result in 
    player 1 horizontal victory.
    """
    # Define required variables
    player1 = Piece("Test1","red", "O", 1)
    player2 = Piece("Test2","blue", "X", 2)
    players = [player1, player2]
    board = Board(players)
    referee = VictoryChecker(board, players)

    # Sequence of user input to achieve the desired sequence of commands
    input_sequence = iter(["1", "1", "2", "2","3", "3", "4"])

    # Replaces default input function to enter input_sequence in sequence
    monkeypatch.setattr("builtins.input", lambda _: next(input_sequence))
    
    # Main function
    result = game_in_progress(board, players, referee)

    # Function should return player 1 as a winner, with no surrendered players
    assert result == (player1, None)


def test_game_in_progress_p1wins_diagonal_victory(monkeypatch):
    """
    Tests the following sequence during game_in_progress: players 1 and 2
    taking turns to ensure player 1 wins with a diagonal victory from the following
    slots (row, column): (1, 1), (2, 2), (3, 3), (4, 4).
    """
    # Define required variables
    player1 = Piece("Test1","red", "O", 1)
    player2 = Piece("Test2","blue", "X", 2)
    players = [player1, player2]
    board = Board(players)
    referee = VictoryChecker(board, players)

    # Sequence of user input to achieve the desired sequence of commands
    input_sequence = iter(["1", "2", "2", "3", "4", "3", "3", "4", "5", "4", "4"])

    # Replaces default input function to enter input_sequence in sequence
    monkeypatch.setattr("builtins.input", lambda _: next(input_sequence))
    
    # Main function
    result = game_in_progress(board, players, referee)

    # Function should return player 1 as a winner, with no surrendered players
    assert result == (player1, None)


def test_game_in_progress_draw(monkeypatch):
    """
    Tests the following sequence during game_in_progress: player 1 and player 2
    putting pieces during their turn in a way that causes none of them to win
    until the board is full, causing a draw.
    """
    # Define required variables
    player1 = Piece("Test1","red", "O", 1)
    player2 = Piece("Test2","blue", "X", 2)
    players = [player1, player2]
    board = Board(players)
    referee = VictoryChecker(board, players)

    # Sequence of user input to achieve the desired sequence of commands
    listing = (
        ['1', '2'] * 3 + ['2', '1'] * 3 + ['3', '4'] * 3 + ['4', '3'] * 3
        + ['5', '6'] * 3  + ['6', '5'] * 3 + ['7'] * 6
    )
    input_sequence = iter(listing)

    # Replaces default input function to enter input_sequence in sequence
    monkeypatch.setattr("builtins.input", lambda _: next(input_sequence))

    # Main function
    result = game_in_progress(board, players, referee)

    # Function should return no winners and no surrenders as it is a draw.
    assert result == (None, None)


def test_game_in_progress_surrender(monkeypatch):
    """
    Tests the surrender command.
    """
    # Required variables
    player1 = Piece("Test1","red", "O", 1)
    player2 = Piece("Test2","blue", "X", 2)
    players = [player1, player2]
    board = Board(players)
    referee = VictoryChecker(board, players)

    # Automatically inputs "surrender"during the first player 1's turn
    input_sequence = iter(["surrender"])

    # Replaces default input function to enter input_sequence in sequence
    monkeypatch.setattr("builtins.input", lambda _: next(input_sequence))

    # Main function
    result = game_in_progress(board, players, referee)

    # Function should return player 2 as the winner and player 1 as the
    # surrendering player.
    assert result == (player2, player1)

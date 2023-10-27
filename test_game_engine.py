import pytest
from game_engine import game_in_progress
from game_board import Board, Piece
from win_conditions import VictoryChecker


def test_game_in_progress_p1wins(monkeypatch):
    player1 = Piece("Test1","red", "O", 1)
    player2 = Piece("Test2","blue", "X", 2)
    players = [player1, player2]
    board = Board(players)
    referee = VictoryChecker(board, players)

    input_sequence = iter(["1", "2", "1", "2","1", "2", "1"])
    monkeypatch.setattr("builtins.input", lambda _: next(input_sequence))
    result = game_in_progress(board, players, referee)
    assert result == (player1, None)


def test_game_in_progress_draw(monkeypatch):
    player1 = Piece("Test1","red", "O", 1)
    player2 = Piece("Test2","blue", "X", 2)
    players = [player1, player2]
    board = Board(players)
    referee = VictoryChecker(board, players)

    list = (
        ['1', '2'] * 3 + ['2', '1'] * 3 + ['3', '4'] * 3 + ['4', '3'] * 3
        + ['5', '6'] * 3  + ['6', '5'] * 3 + ['7'] * 6
    )

    input_sequence = iter(list)

    monkeypatch.setattr("builtins.input", lambda _: next(input_sequence))
    result = game_in_progress(board, players, referee)
    assert result == (None, None)


def test_game_in_progress_surrender(monkeypatch):
    player1 = Piece("Test1","red", "O", 1)
    player2 = Piece("Test2","blue", "X", 2)
    players = [player1, player2]
    board = Board(players)
    referee = VictoryChecker(board, players)

    input_sequence = iter(["surrender"])

    monkeypatch.setattr("builtins.input", lambda _: next(input_sequence))
    result = game_in_progress(board, players, referee)
    assert result == (player2, player1)


import pytest
from hubs import PlayerLounge, MainLobby, GameHub
from game_board import Board, Piece


def test_player_lounge_enter(monkeypatch):
    player1 = Piece("Test1","red", "O", 1)
    player2 = Piece("Test2","blue", "X", 2)
    players = [player1, player2]


    sequence = 

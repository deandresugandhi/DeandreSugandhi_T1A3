"""
Module to test important functions from utilities.py
"""

import pytest
from utilities import validate_input, validate_username


def test_validate_input_valid(monkeypatch):
    """
    Tests validate_input, inputting a valid input.
    """
    # Required variables:
    prompt = "Valid username: "
    # 5-20 characters, alphanumeric + period + underscore, starts and ends
    # with alphanumeric character.
    match = "^[a-zA-Z0-9][a-zA-Z0-9._-]{3,18}[a-zA-Z0-9]$"

    # User input that should be valid
    user_input = "tester123"
    input_sequence = iter([user_input])

    # Replaces default input function to enter input_sequence in sequence
    monkeypatch.setattr("builtins.input", lambda _: next(input_sequence))

    # Main function
    result = validate_input(
        prompt = prompt,
        match = match
    )

    # Function should return user_input as it is valid
    assert result == user_input


def test_validate_input_invalid(monkeypatch):
    """
    Tests validate_input, inputting an invalid input.
    """
    # Required variables:
    prompt = "Valid username: "
    # 5-20 characters, alphanumeric + period + underscore, starts and ends
    # with alphanumeric character.
    match = "^[a-zA-Z0-9][a-zA-Z0-9._-]{3,18}[a-zA-Z0-9]$"

    # Invalid user input should be inputted first, then a valid input to exit
    # the function properly. If invalid input is not detected, the test should
    # fail because it is not expecting another input.
    invalid_input = "__tester123__"
    valid_input = "tester123"
    input_sequence = iter([invalid_input, valid_input])

    # Replaces default input function to enter input_sequence in sequence
    monkeypatch.setattr("builtins.input", lambda _: next(input_sequence))

    # Main function
    result = validate_input(
            prompt = prompt,
            match = match
        )

    # Function should return user_input as last input is valid
    assert result == valid_input


def test_validate_username_valid(monkeypatch):
    """
    Tests validate_username, inputting a valid input.
    """
    # Required variables:
    prompt = "Valid username: "
    # 5-20 characters, alphanumeric + period + underscore, starts and ends
    # with alphanumeric character.
    match = "^[a-zA-Z0-9][a-zA-Z0-9._-]{3,18}[a-zA-Z0-9]$"

    # User input that should be valid, as tester000 is not taken in users.json,
    # as of current test.
    user_input = "tester000"
    input_sequence = iter([user_input])

    # Replaces default input function to enter input_sequence in sequence
    monkeypatch.setattr("builtins.input", lambda _: next(input_sequence))

    # Main function
    result = validate_username(
        prompt = prompt,
        match = match
    )

    # Function should return user_input as it is valid
    assert result == user_input


def test_validate_username_invalid(monkeypatch):
    """
    Tests validate_username, inputting an invalid input.
    """
    # Required variables:
    prompt = "Valid username: "
    # 5-20 characters, alphanumeric + period + underscore, starts and ends
    # with alphanumeric character.
    match = "^[a-zA-Z0-9][a-zA-Z0-9._-]{3,18}[a-zA-Z0-9]$"

    # Invalid user input should be inputted first, then a valid input to exit
    # the function properly. If invalid input is not detected, the test should
    # fail because it is not expecting another input. first is invalid because
    # tester123 exists already in users.json and is thus a duplicate.
    invalid_input = "tester123"
    valid_input = "tester000"
    input_sequence = iter([invalid_input, valid_input])

    # Replaces default input function to enter input_sequence in sequence
    monkeypatch.setattr("builtins.input", lambda _: next(input_sequence))

    # Main function
    result = validate_username(
            prompt = prompt,
            match = match
        )

    # Function should return user_input as last input is valid
    assert result == valid_input

"""Test that the parser correctly parses factors."""

import pyparsing.exceptions

import parse


def test_factor_single_atom():
    """Test that a single atom parses as a factor."""
    parser = parse.Parser()
    try:
        parser.consume_factor("(hello)")
    except pyparsing.exceptions.ParseBaseException:
        assert False


def test_factor_atom_exp():
    """Test that a single atom with an exponent parses."""
    parser = parse.Parser()
    try:
        parser.consume_factor("(hello) ^ (1234.7890)")
    except pyparsing.exceptions.ParseBaseException:
        assert False


def test_factor_atom_two_exp():
    """Test that a single atom with an exponent parses."""
    parser = parse.Parser()
    try:
        parser.consume_factor("(hello) ^ (1234.7890) ^ (my_var)")
    except pyparsing.exceptions.ParseBaseException:
        assert False


def test_factor_atom_nexted_exp_in_parens():
    """Test that a single atom with an exponent parses."""
    parser = parse.Parser()
    try:
        parser.consume_factor("(hello) ^ (1234.7890 ^ 4) ^ (my_var)")
    except pyparsing.exceptions.ParseBaseException:
        assert False


def test_factor_atom_mismatch_parens():
    """Test that a single atom with an exponent parses."""
    parser = parse.Parser()
    try:
        parser.consume_factor("(hello) ^ (1234.7890 ^ 4 ^ (my_var)")
    except pyparsing.exceptions.ParseBaseException:
        return

    assert False

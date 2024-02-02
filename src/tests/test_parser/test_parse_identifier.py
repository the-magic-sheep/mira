"""Test that the parser correctly parses identifiers."""

import pyparsing.exceptions

import parse


def test_ident_single_char():
    """Test that a single char identifier parses correctly."""
    parser = parse.Parser()
    try:
        parser.consume_ident("x")
    except pyparsing.ParseBaseException:
        assert False


def test_ident_single_uscore():
    """Test that a single underscore identifier parses correctly."""
    parser = parse.Parser()
    try:
        parser.consume_ident("_")
    except pyparsing.ParseBaseException:
        assert False


def test_ident_single_digit():
    """Test that a single digit identifier does not parse."""
    parser = parse.Parser()
    try:
        parser.consume_ident("0")
    except pyparsing.ParseBaseException:
        return

    assert False


def test_ident_full():
    """Test that an identifier parses correctly."""
    parser = parse.Parser()
    try:
        parser.consume_ident("_0fadf_324")
    except pyparsing.ParseBaseException:
        assert False

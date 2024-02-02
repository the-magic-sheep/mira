"""Test that the parser correctly parses integer literals."""

import pyparsing.exceptions

import parse


def test_int_single_num():
    """Test that a single char identifier parses correctly."""
    parser = parse.Parser()
    try:
        parser.consume_int("1")
    except pyparsing.ParseBaseException:
        assert False


def test_int_with_dot():
    """Test that a number with a period doesn't parse as an int."""
    parser = parse.Parser()
    try:
        parser.consume_int("1.1234")
    except pyparsing.ParseBaseException:
        return
    assert False


def test_int_dot_first():
    """Test that a number with a period doesn't parse as an int."""
    parser = parse.Parser()
    try:
        parser.consume_int(".1234")
    except pyparsing.ParseBaseException:
        return
    assert False

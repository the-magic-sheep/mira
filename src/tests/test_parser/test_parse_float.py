"""Test that the parser correctly parses number literals."""

import pyparsing.exceptions

import parse


def test_num_single_num():
    """Test that a single digit number doesn't parse."""
    parser = parse.Parser()
    try:
        parser.consume_num("1")
    except pyparsing.ParseBaseException:
        return

    assert False


def test_num_single_dot_start():
    """Test that a number starting with a period doesn't parse."""
    parser = parse.Parser()
    try:
        parser.consume_num(".1123")
    except pyparsing.ParseBaseException:
        return

    assert False


def test_num_single_dot_end():
    """Test that a number ending with a period parses."""
    parser = parse.Parser()
    try:
        parser.consume_num("123.")
    except pyparsing.ParseBaseException:
        assert False


def test_num_two_dots():
    """Test that a number with two periods doesn't parse."""
    parser = parse.Parser()
    try:
        parser.consume_num("123.5432.543")
    except pyparsing.ParseBaseException:
        return
    assert False


def test_num_full():
    """Test that a number parses correctly."""
    parser = parse.Parser()
    try:
        parser.consume_num("123.5431")
    except pyparsing.ParseBaseException:
        assert False

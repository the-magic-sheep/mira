"""Test that the parser correctly parses terms."""

import pyparsing.exceptions

import parse


def test_varset_int():
    """Test that a variable set parses with an int."""
    parser = parse.Parser()
    try:
        parser.consume_var_set("x = 5")
    except pyparsing.exceptions.ParseBaseException:
        assert False


def test_varset_num():
    """Test that a variable set parses with a num."""
    parser = parse.Parser()
    try:
        parser.consume_var_set("x = 5.6")
    except pyparsing.exceptions.ParseBaseException:
        assert False


def test_varset_var():
    """Test that a variable set parses with a variable"""
    parser = parse.Parser()
    try:
        parser.consume_var_set("x = y")
    except pyparsing.exceptions.ParseBaseException:
        assert False


def test_varset_math():
    """Test that a variable set parses with an expression."""
    parser = parse.Parser()
    try:
        parser.consume_var_set("x = y * 0.543 + 2 ^ my_var")
    except pyparsing.exceptions.ParseBaseException:
        assert False

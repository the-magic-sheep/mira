"""Test that the parser correctly parses terms."""

import pyparsing.exceptions

import parse


def test_term_single_factor():
    """Test that a single factor parses as a term."""
    parser = parse.Parser()
    try:
        parser.consume_term("(hello ^ 4.654) ^ my_var ^ 1234")
    except pyparsing.exceptions.ParseBaseException:
        assert False


def test_term_single_mul():
    """Test that a single binary multiplication parses as a term."""
    parser = parse.Parser()
    try:
        parser.consume_term("7 * my_var")
    except pyparsing.exceptions.ParseBaseException:
        assert False


def test_term_many_mul():
    """Test that a single binary multiplication parses as a term."""
    parser = parse.Parser()
    parser.consume_term("8 * 5 ^ 5 ^ 3 * (4 ^ 17 * my_var)")

"""Test that the parser correctly parses exprs."""

import pyparsing.exceptions

import parse


def test_expr_single_term():
    """Test that a single term parses as an expr."""
    parser = parse.Parser()
    try:
        parser.consume_expr("5 * 5")
    except pyparsing.exceptions.ParseBaseException:
        assert False


def test_expr_add_terms():
    """Test that addition parses as a expt."""
    parser = parse.Parser()
    try:
        parser.consume_expr("5 * 5 + 5 * 5")
    except pyparsing.exceptions.ParseBaseException:
        assert False


def test_complex_expr():
    """Test that a complex expr parses"""
    parser = parse.Parser()
    try:
        parser.consume_expr("(5 ^ -9) + 5 ^ (3 + 2 * 7^2) - 18 * -47")
    except pyparsing.exceptions.ParseBaseException:
        assert False

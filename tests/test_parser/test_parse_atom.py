"""Test that the parser correctly parses atoms."""

import pyparsing.exceptions

import parse


def test_atom_single_int():
    """Test that a single int parses as an atom."""
    parser = parse.Parser()
    try:
        parser.consume_atom("1343")
    except pyparsing.exceptions.ParseBaseException:
        assert False


def test_factor_single_num():
    """Test that a single number parses as an atom."""
    parser = parse.Parser()
    try:
        parser.consume_atom("1.123")
    except pyparsing.exceptions.ParseBaseException:
        assert False


def test_factor_single_ident():
    """Test that a single ident parses as an atom."""
    parser = parse.Parser()
    try:
        parser.consume_atom("hello_how_are_you123")
    except pyparsing.exceptions.ParseBaseException:
        assert False


def test_factor_single_int_parens():
    """Test that a single ident parses as an atom."""
    parser = parse.Parser()
    try:
        parser.consume_atom("1343")
    except pyparsing.exceptions.ParseBaseException:
        assert False


def test_factor_single_num_parens():
    """Test that a single ident parses as an atom."""
    parser = parse.Parser()
    try:
        parser.consume_atom("1234.5678")
    except pyparsing.exceptions.ParseBaseException:
        assert False

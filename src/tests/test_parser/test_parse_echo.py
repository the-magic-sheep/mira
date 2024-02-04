"""Test that the parser correctly parses echo statements."""

import pyparsing.exceptions

import parse


def test_echo_ident():
    """Test that echo ident parses correctly."""
    parser = parse.Parser()
    try:
        parser.consume_echo("echo x")
    except pyparsing.exceptions.ParseBaseException:
        assert False


def test_echo_num():
    """Test that echo num parses correctly."""
    parser = parse.Parser()
    try:
        parser.consume_echo("echo 4.5")
    except pyparsing.exceptions.ParseBaseException:
        assert False


def test_echo_int():
    """Test that echo int parses correctly."""
    parser = parse.Parser()
    try:
        parser.consume_echo("echo 1")
    except pyparsing.exceptions.ParseBaseException:
        assert False


def test_echo_expr():
    """Test that echo int parses correctly."""
    parser = parse.Parser()
    try:
        parser.consume_echo("echo x + y + 4 ^ 7 ^ (-4 * 1234.5678)")
    except pyparsing.exceptions.ParseBaseException:
        assert False

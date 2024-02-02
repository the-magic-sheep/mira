"""Test that the parser correctly parses terms."""

import pyparsing.exceptions

import parse


def test_vardef_explicit_int():
    """Test that a variable definition parses with an int."""
    parser = parse.Parser()
    try:
        parser.consume_var_def("x:int = 5")
    except pyparsing.exceptions.ParseBaseException:
        assert False


def test_vardef_explicit_num():
    """Test that a variable definition parses with a num."""
    parser = parse.Parser()
    try:
        parser.consume_var_def("x:num = 25.7")
    except pyparsing.exceptions.ParseBaseException:
        assert False


def test_vardef_explicit_var():
    """Test that a variable definition parses with a var."""
    parser = parse.Parser()
    try:
        parser.consume_var_def("x:num = y")
    except pyparsing.exceptions.ParseBaseException:
        assert False


def test_vardef_explicit_expr():
    """Test that a variable definition parses with an expression."""
    parser = parse.Parser()
    try:
        parser.consume_var_def("x:num = 5 + 35*my_var ^ -13.5")
    except pyparsing.exceptions.ParseBaseException:
        assert False


def test_vardef_implicit_int():
    """Test that an implicit variable definition parses with an int."""
    parser = parse.Parser()
    try:
        parser.consume_var_def("x: = 5")
    except pyparsing.exceptions.ParseBaseException:
        assert False


def test_vardef_implicit_num():
    """Test that an implicit variable definition parses with a num."""
    parser = parse.Parser()
    try:
        parser.consume_var_def("x: = 25.7")
    except pyparsing.exceptions.ParseBaseException:
        assert False


def test_vardef_implicit_var():
    """Test that an implicit variable definition parses with a var."""
    parser = parse.Parser()
    try:
        parser.consume_var_def("x: = y")
    except pyparsing.exceptions.ParseBaseException:
        assert False


def test_vardef_implicit_expr():
    """Test that an implicit variable definition parses with an expression."""
    parser = parse.Parser()
    try:
        parser.consume_var_def("x: = 5 + 35*my_var ^ -13.5")
    except pyparsing.exceptions.ParseBaseException:
        assert False

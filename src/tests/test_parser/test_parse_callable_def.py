"""Module providing tests for callable type definitions."""

import pyparsing

import parse


def test_single_param_paramlist():
    parser = parse.Parser()
    try:
        parser.consume_paramlist("test: type1")
    except pyparsing.exceptions.ParseBaseException:
        assert False


def test_full_paramlist():
    parser = parse.Parser()
    try:
        parser.consume_paramlist("test: type1, test2: type2, test3: type3")
    except pyparsing.exceptions.ParseBaseException:
        assert False


def test_paramlist_comma_after():
    parser = parse.Parser()
    try:
        parser.consume_paramlist("test: type1, test2: type2, test3: type3,")
    except pyparsing.exceptions.ParseBaseException:
        assert False


def test_callable_no_paramslist():
    parser = parse.Parser()
    try:
        parser.consume_callable("test()")
    except pyparsing.exceptions.ParseBaseException:
        assert False


def test_callable_single_param_paramlist():
    parser = parse.Parser()
    try:
        parser.consume_callable("int(test: type1)")
    except pyparsing.exceptions.ParseBaseException:
        assert False


def test_callable_full_paramlist():
    parser = parse.Parser()
    try:
        parser.consume_callable("int(test: type1, test2: type2, test3: type3)")
    except pyparsing.exceptions.ParseBaseException:
        assert False


def test_callable_paramlist_comma_after():
    parser = parse.Parser()
    try:
        parser.consume_callable("int(test: type1, test2: type2, test3: type3,)")
    except pyparsing.exceptions.ParseBaseException:
        assert False

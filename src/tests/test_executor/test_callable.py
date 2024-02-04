from typing import Any

import execute
import parse


def test_simple_paramlist():
    parser = parse.Parser()
    executor = execute.Executor()

    parsed = parser.consume_paramlist("param1: int")["children"][0]
    result: Any = executor.exec([parsed])
    assert result == {"param1": execute.Int}


def test_long_paramlist():
    parser = parse.Parser()
    executor = execute.Executor()

    parsed = parser.consume_paramlist("param1: int, param2: num, param3: int")[
        "children"
    ][0]
    result: Any = executor.exec([parsed])
    assert result == {
        "param1": execute.Int,
        "param2": execute.Num,
        "param3": execute.Int,
    }


def test_long_paramlist_comma_after():
    parser = parse.Parser()
    executor = execute.Executor()

    parsed = parser.consume_paramlist("param1: int, param2: num, param3: int,")[
        "children"
    ][0]
    result: Any = executor.exec([parsed])
    assert result == {
        "param1": execute.Int,
        "param2": execute.Num,
        "param3": execute.Int,
    }


def test_long_paramlist_invalid_type():
    parser = parse.Parser()
    executor = execute.Executor()

    parsed = parser.consume_paramlist("param1: invalid_type")["children"][0]
    try:
        executor.exec([parsed])
    except SyntaxError:
        return

    assert False

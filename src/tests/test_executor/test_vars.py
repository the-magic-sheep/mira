from typing import Any

import execute
import parse


def test_define_var():
    parser = parse.Parser()
    executor = execute.Executor()

    executor.exec(parser.parse("x: int = 10"))
    assert (
        executor.globals["x"].value == 10
        and isinstance(executor.globals["x"].value, int)
        and isinstance(executor.globals["x"], execute.Int)
    )


def test_use_undefined():
    parser = parse.Parser()
    executor = execute.Executor()
    try:
        executor.exec(parser.parse("5 + x"))
    except SyntaxError:
        return

    assert False, "Failed to throw error for undefined variable usage."


def test_use_defined():
    parser = parse.Parser()
    executor = execute.Executor()

    executor.exec(parser.parse("x: int = 10"))
    result: Any = executor.exec(parser.parse("5 + x"))
    assert (
        result.value == 15
        and isinstance(result.value, int)
        and isinstance(result, execute.Int)
    )


def test_redefine():
    parser = parse.Parser()
    executor = execute.Executor()

    executor.exec(parser.parse("x: int = 10"))
    executor.exec(parser.parse("x: num = 10"))

    assert (
        executor.globals["x"].value == 10.0
        and isinstance(executor.globals["x"].value, float)
        and isinstance(executor.globals["x"], execute.Num)
    )


def test_recursive_redefine():
    parser = parse.Parser()
    executor = execute.Executor()

    executor.exec(parser.parse("x: int = 10"))
    executor.exec(parser.parse("x: num = x + 5"))
    assert executor.globals["x"].value == 15.0 and isinstance(
        executor.globals["x"], execute.Num
    )


def test_set_same_type():
    parser = parse.Parser()
    executor = execute.Executor()

    executor.exec(parser.parse("x: int = 10"))
    executor.exec(parser.parse("x = 5"))
    assert (
        executor.globals["x"].value == 5
        and isinstance(executor.globals["x"].value, int)
        and isinstance(executor.globals["x"], execute.Int)
    )


def test_set_different_type():
    parser = parse.Parser()
    executor = execute.Executor()

    executor.exec(parser.parse("x: int = 10"))
    executor.exec(parser.parse("x = 5.0"))
    assert (
        executor.globals["x"].value == 5
        and isinstance(executor.globals["x"].value, int)
        and isinstance(executor.globals["x"], execute.Int)
    )


def test_inference_int():
    parser = parse.Parser()
    executor = execute.Executor()

    executor.exec(parser.parse("x: = 10"))
    assert (
        executor.globals["x"].value == 10
        and isinstance(executor.globals["x"].value, int)
        and isinstance(executor.globals["x"], execute.Int)
    )


def test_inference_num():
    parser = parse.Parser()
    executor = execute.Executor()

    executor.exec(parser.parse("x: = 10."))
    assert (
        executor.globals["x"].value == 10.0
        and isinstance(executor.globals["x"].value, float)
        and isinstance(executor.globals["x"], execute.Num)
    )


def test_inference_int_from_var():
    parser = parse.Parser()
    executor = execute.Executor()

    executor.exec(parser.parse("x: = 10"))
    executor.exec(parser.parse("y: = x"))
    assert (
        executor.globals["y"].value == 10
        and isinstance(executor.globals["y"].value, int)
        and isinstance(executor.globals["y"], execute.Int)
    )


def test_inference_num_from_var():
    parser = parse.Parser()
    executor = execute.Executor()

    executor.exec(parser.parse("x: = 10."))
    executor.exec(parser.parse("y: = x"))
    assert (
        executor.globals["y"].value == 10.0
        and isinstance(executor.globals["y"].value, float)
        and isinstance(executor.globals["y"], execute.Num)
    )


def test_inference_int_redefine_recursive():
    parser = parse.Parser()
    executor = execute.Executor()

    executor.exec(parser.parse("x: = 10"))
    executor.exec(parser.parse("x: = x + 0."))
    assert (
        executor.globals["x"].value == 10.0
        and isinstance(executor.globals["x"].value, float)
        and isinstance(executor.globals["x"], execute.Num)
    )

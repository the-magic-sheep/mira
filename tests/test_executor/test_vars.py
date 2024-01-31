import execute
import parse


def test_define_var():
    parser = parse.Parser()
    executor = execute.Executor()

    executor.exec(parser.parse("x: int = 10"))
    assert (
        executor.globals["x"].value == 10
        and isinstance(executor.globals["x"].value, int)
        and executor.globals["x"].type is execute.Types.INT
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
    result = executor.exec(parser.parse("5 + x"))
    assert result == 15 and isinstance(result, int)


def test_redefine():
    parser = parse.Parser()
    executor = execute.Executor()

    executor.exec(parser.parse("x: int = 10"))
    executor.exec(parser.parse("x: num = 10"))
    assert (
        executor.globals["x"].value == 10.0
        and isinstance(executor.globals["x"].value, float)
        and executor.globals["x"].type is execute.Types.NUM
    )


def test_recursive_redefine():
    parser = parse.Parser()
    executor = execute.Executor()

    executor.exec(parser.parse("x: int = 10"))
    executor.exec(parser.parse("x: num = x + 5"))
    assert (
        executor.globals["x"].value == 15.0
        and isinstance(executor.globals["x"].value, float)
        and executor.globals["x"].type is execute.Types.NUM
    )


def test_set_same_type():
    parser = parse.Parser()
    executor = execute.Executor()

    executor.exec(parser.parse("x: int = 10"))
    executor.exec(parser.parse("x = 5"))
    assert (
        executor.globals["x"].value == 5
        and isinstance(executor.globals["x"].value, int)
        and executor.globals["x"].type is execute.Types.INT
    )


def test_set_different_type():
    parser = parse.Parser()
    executor = execute.Executor()

    executor.exec(parser.parse("x: int = 10"))
    executor.exec(parser.parse("x = 5.0"))
    assert (
        executor.globals["x"].value == 5
        and isinstance(executor.globals["x"].value, int)
        and executor.globals["x"].type is execute.Types.INT
    )

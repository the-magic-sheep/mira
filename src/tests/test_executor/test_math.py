from typing import Any

import execute
import parse


def test_add():
    parser = parse.Parser()
    executor = execute.Executor()

    result: Any = executor.exec(parser.parse("5 + 5"))
    assert result.value == 10 and isinstance(result, execute.Int)


def test_add_num():
    parser = parse.Parser()
    executor = execute.Executor()

    result_a: Any = executor.exec(parser.parse("5 + 5."))
    result_b: Any = executor.exec(parser.parse("5. + 5"))
    assert (
        result_a.value == 10.0 == result_b.value
        and isinstance(result_a, execute.Num)
        and isinstance(result_b, execute.Num)
    )


def test_multiply():
    parser = parse.Parser()
    executor = execute.Executor()

    result: Any = executor.exec(parser.parse("5 * 5"))
    assert result.value == 25 and isinstance(result, execute.Int)


def test_multipy_num():
    parser = parse.Parser()
    executor = execute.Executor()

    result_a: Any = executor.exec(parser.parse("5 * 5."))
    result_b: Any = executor.exec(parser.parse("5. * 5"))
    assert (
        result_a.value == 25.0 == result_b.value
        and isinstance(result_a, execute.Num)
        and isinstance(result_b, execute.Num)
    )


def test_subtract():
    parser = parse.Parser()
    executor = execute.Executor()

    result: Any = executor.exec(parser.parse("25 - 5"))
    assert result.value == 20 and isinstance(result, execute.Int)


def test_subtract_num():
    parser = parse.Parser()
    executor = execute.Executor()

    result_a: Any = executor.exec(parser.parse("25 - 5."))
    result_b: Any = executor.exec(parser.parse("25. - 5"))
    assert (
        result_a.value == 20.0 == result_b.value
        and isinstance(result_a, execute.Num)
        and isinstance(result_b, execute.Num)
    )


def test_divide():
    parser = parse.Parser()
    executor = execute.Executor()

    result: Any = executor.exec(parser.parse("25 / 5"))
    assert result.value == 5 and isinstance(result, execute.Int)


def test_divide_num():
    parser = parse.Parser()
    executor = execute.Executor()

    result_a: Any = executor.exec(parser.parse("25 / 5."))
    result_b: Any = executor.exec(parser.parse("25. / 5"))
    assert (
        result_a.value == 5.0 == result_b.value
        and isinstance(result_a, execute.Num)
        and isinstance(result_b, execute.Num)
    )


def test_exponentiation():
    parser = parse.Parser()
    executor = execute.Executor()

    result: Any = executor.exec(parser.parse("25 ^ 5"))
    assert result.value == 25**5 and isinstance(result, execute.Int)


def test_exponentiation_num():
    parser = parse.Parser()
    executor = execute.Executor()

    result_a: Any = executor.exec(parser.parse("25. ^ 5"))
    result_b: Any = executor.exec(parser.parse("25 ^ 5."))
    assert (
        result_a.value == 25.0**5.0 == result_b.value
        and isinstance(result_a, execute.Num)
        and isinstance(result_b, execute.Num)
    )


def test_complex_expr():
    parser = parse.Parser()
    executor = execute.Executor()

    result: Any = executor.exec(
        parser.parse(
            """
                5 + 5 * (4 - 31 ^ 3 ^ 2 / (3 * 10 ^ 8)) / 7 + -2*10^5
            """
        )
    )

    assert result.value == int(
        5 + 5 * (4 - 31**3**2 / (3 * 10**8)) / 7 + -2 * 10**5
    ) and isinstance(result, execute.Int)


def test_complex_num():
    parser = parse.Parser()
    executor = execute.Executor()

    result: Any = executor.exec(
        parser.parse(
            """
                5 + 5 * (4 - 31. ^ 3 ^ 2 / (3 * 10 ^ 8)) / 7 / 3.^-2 + -2*10^5
            """
        )
    )

    assert result.value == float(
        5 + 5 * (4 - 31**3**2 / (3 * 10**8)) / 7 / 3**-2 + -2 * 10**5
    ) and isinstance(result, execute.Num)

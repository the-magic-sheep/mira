import execute
import parse


def test_add():
    parser = parse.Parser()
    executor = execute.Executor()

    result = executor.exec(parser.parse("5 + 5"))
    assert result == 10 and isinstance(result, int)


def test_add_float():
    parser = parse.Parser()
    executor = execute.Executor()

    result_a = executor.exec(parser.parse("5 + 5."))
    result_b = executor.exec(parser.parse("5. + 5"))
    assert (
        result_a == 10.0 == result_b
        and isinstance(result_a, float)
        and isinstance(result_b, float)
    )


def test_multiply():
    parser = parse.Parser()
    executor = execute.Executor()

    result = executor.exec(parser.parse("5 * 5"))
    assert result == 25 and isinstance(result, int)


def test_multipy_float():
    parser = parse.Parser()
    executor = execute.Executor()

    result_a = executor.exec(parser.parse("5 * 5."))
    result_b = executor.exec(parser.parse("5. * 5"))
    assert (
        result_a == 25.0 == result_b
        and isinstance(result_a, float)
        and isinstance(result_b, float)
    )


def test_subtract():
    parser = parse.Parser()
    executor = execute.Executor()

    result = executor.exec(parser.parse("25 - 5"))
    assert result == 20 and isinstance(result, int)


def test_subtract_float():
    parser = parse.Parser()
    executor = execute.Executor()

    result_a = executor.exec(parser.parse("25 - 5."))
    result_b = executor.exec(parser.parse("25. - 5"))
    assert (
        result_a == 20.0 == result_b
        and isinstance(result_a, float)
        and isinstance(result_b, float)
    )


def test_divide():
    parser = parse.Parser()
    executor = execute.Executor()

    result = executor.exec(parser.parse("25 / 5"))
    assert result == 5 and isinstance(result, float)


def test_divide_float():
    parser = parse.Parser()
    executor = execute.Executor()

    result_a = executor.exec(parser.parse("25 / 5."))
    result_b = executor.exec(parser.parse("25. / 5"))
    assert (
        result_a == 5.0 == result_b
        and isinstance(result_a, float)
        and isinstance(result_b, float)
    )


def test_exponentiation():
    parser = parse.Parser()
    executor = execute.Executor()

    result = executor.exec(parser.parse("25 ^ 5"))
    assert result == 25**5 and isinstance(result, int)


def test_exponentiation_float():
    parser = parse.Parser()
    executor = execute.Executor()

    result_a = executor.exec(parser.parse("25. ^ 5"))
    result_b = executor.exec(parser.parse("25 ^ 5."))
    assert (
        result_a == 25.0**5.0 == result_b
        and isinstance(result_a, float)
        and isinstance(result_b, float)
    )


def test_complex_expr():
    parser = parse.Parser()
    executor = execute.Executor()

    result = executor.exec(
        parser.parse(
            """
                5 + 5 * (4 - 31 ^ 3 ^ 2 / (3 * 10 ^ -8)) / 7 / 3^-2 + -2*10^5
            """
        )
    )

    assert result == float(
        5 + 5 * (4 - 31**3**2 / (3 * 10**-8)) / 7 / 3**-2 + -2 * 10**5
    )

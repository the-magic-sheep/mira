from typing import Any

import pyparsing as pp

import literals


def results_to_list(
    parse_result: pp.ParseResults | list[dict[str, Any]] | Any,
) -> list[dict[str, Any]] | dict[str, Any]:
    if isinstance(parse_result, pp.ParseResults):
        flat_results: list[Any] = parse_result.as_list()
    else:
        flat_results: list[Any] = parse_result.copy()

    for ii, res in enumerate(flat_results):
        res: pp.ParseResults | list[dict[str, Any]] | Any
        if isinstance(res, pp.ParseResults):
            flat_results[ii] = results_to_list(res)

        elif isinstance(res, list):
            if len(res) == 1 and isinstance(res[0], list):
                flat_results[ii] = results_to_list(res[0])
            else:
                for jj, res2 in enumerate(res):
                    if isinstance(res2, (pp.ParseResults, list)):
                        flat_results[ii][jj] = results_to_list(res2)

    return flat_results


class Parser:

    def __init__(self):
        self.int = pp.Regex(r"[+-]?[0-9]+")
        self.int.add_parse_action(self.consume_int)
        self.num = pp.Regex(r"[+-]?\d+(\.\d*|[eE][+-]?\d+)")
        self.num.add_parse_action(self.consume_num)
        self.ident = pp.Regex(r"[_a-zA-Z]+[_a-zA-Z0-9]*")
        self.ident.add_parse_action(self.consume_ident)

        self.plus = pp.Literal(literals.OP_ADD)
        self.minus = pp.Literal(literals.OP_SUB)
        self.mult = pp.Literal(literals.OP_MUL)
        self.div = pp.Literal(literals.OP_DIV)
        self.exp = pp.Literal(literals.OP_EXP)

        self.lparen = pp.Literal(literals.L_PAREN)
        self.rparen = pp.Literal(literals.R_PAREN)

        self.op_prec = [self.plus | self.minus, self.mult | self.div, self.exp]

        self.expr = pp.Forward()
        self.expr_list = pp.delimited_list(pp.Group(self.expr))

        self.atom = (self.num | self.int | self.ident) | (
            self.lparen + self.expr + self.rparen
        )
        self.atom.add_parse_action(self.consume_atom)

        self.factor = pp.Forward()
        self.factor <<= self.atom + pp.ZeroOrMore(self.op_prec[-1] + self.factor)
        self.factor.add_parse_action(self.consume_factor)

        self.term = self.factor + pp.ZeroOrMore(self.op_prec[-2] + self.factor)
        self.term.add_parse_action(self.consume_term)

        self.expr <<= self.term + pp.ZeroOrMore(self.op_prec[-3] + self.term)
        self.expr.add_parse_action(self.consume_expr)

        self.var_def = self.ident + ":" + self.ident + "=" + self.expr
        self.var_def.add_parse_action(self.consume_var_def)

        self.var_set = self.ident + "=" + self.expr
        self.var_set.add_parse_action(self.consume_var_set)

        self.prog = self.var_def | self.var_set | self.expr

        self.ast: list[dict[str, Any]] = []

    def consume_ident(
        self,
        input_str: str,
        column: int = 0,
        parse_result: pp.ParseResults | None = None,
    ):
        """Parse a given string for an identifier."""
        if parse_result is None:
            parse_result = self.ident.parse_string(input_str, parse_all=True)

        new_ast: dict[str, Any] = {
            "col": column,
            "children": parse_result[0],
            "type": "ident",
        }

        return new_ast

    def consume_int(
        self,
        input_str: str,
        column: int = 0,
        parse_result: pp.ParseResults | None = None,
    ):
        """Parse a given string for an integer literal."""
        if parse_result is None:
            parse_result = self.int.parse_string(input_str, parse_all=True)

        new_ast: dict[str, Any] = {
            "col": column,
            "children": parse_result[0],
            "type": "int",
        }

        return new_ast

    def consume_num(
        self,
        input_str: str,
        column: int = 0,
        parse_result: pp.ParseResults | None = None,
    ):
        """Parse a given string for a number literal."""
        if parse_result is None:
            parse_result = self.num.parse_string(input_str, parse_all=True)

        new_ast: dict[str, Any] = {
            "col": column,
            "children": parse_result[0],
            "type": "num",
        }

        return new_ast

    def consume_atom(
        self,
        input_str: str,
        column: int = 0,
        parse_result: pp.ParseResults | None = None,
    ):
        """Parse a given string for an atom."""
        if parse_result is None:
            parse_result = self.atom.parse_string(input_str, parse_all=True)

        new_ast: dict[str, Any] = {
            "col": column,
            "children": results_to_list(parse_result),
            "type": "atom",
        }

        return new_ast

    def consume_factor(
        self,
        input_str: str,
        column: int = 0,
        parse_result: pp.ParseResults | None = None,
    ):
        """Parse a given string for a factor."""
        if parse_result is None:
            parse_result = self.factor.parse_string(input_str, parse_all=True)

        new_ast: dict[str, Any] = {
            "col": column,
            "children": results_to_list(parse_result),
            "type": "factor",
        }

        return new_ast

    def consume_term(
        self,
        input_str: str,
        column: int = 0,
        parse_result: pp.ParseResults | None = None,
    ):
        """Parse a given string for a term."""
        if parse_result is None:
            parse_result = self.term.parse_string(input_str, parse_all=True)

        new_ast: dict[str, Any] = {
            "col": column,
            "children": results_to_list(parse_result),
            "type": "term",
        }

        return new_ast

    def consume_expr(
        self,
        input_str: str,
        column: int = 0,
        parse_result: pp.ParseResults | None = None,
    ):
        """Parse a given string for an expr."""
        if parse_result is None:
            parse_result = self.expr.parse_string(input_str, parse_all=True)

        new_ast: dict[str, Any] = {
            "col": column,
            "children": results_to_list(parse_result),
            "type": "expr",
        }

        return new_ast

    def consume_var_def(
        self,
        input_str: str,
        column: int = 0,
        parse_result: pp.ParseResults | None = None,
    ):
        """Parse a given string for a variable definition."""
        if parse_result is None:
            parse_result = self.var_def.parse_string(input_str, parse_all=True)

        new_ast: dict[str, Any] = {
            "col": column,
            "children": results_to_list(parse_result),
            "type": "vardef",
        }

        return new_ast

    def consume_var_set(
        self,
        input_str: str,
        column: int = 0,
        parse_result: pp.ParseResults | None = None,
    ):
        """Parse a given string for a variable definition."""
        if parse_result is None:
            parse_result = self.var_set.parse_string(input_str, parse_all=True)

        new_ast: dict[str, Any] = {
            "col": column,
            "children": results_to_list(parse_result),
            "type": "varset",
        }

        return new_ast

    def parse(self, input_str: str) -> Any:
        """Run the parser on the input string."""
        return results_to_list(
            self.prog.parse_string(input_str, parse_all=True).as_list()[0]
        )

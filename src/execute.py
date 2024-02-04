"""Module providing the interpreter"""

from typing import Any, Union

import literals


class Val:
    value: Any

    def __str__(self):
        return str(self.value)

    def _raise_binary(self, op_name: str, other: Any):
        raise SyntaxError(
            f"{op_name} not supported for between type\n"
            + f"{type(self)} and type {type(other)}.\n"
        )

    def add(self, other: Any) -> Any:
        _ = other
        self._raise_binary("Addition", other)

    def sub(self, other: Any) -> Any:
        _ = other
        self._raise_binary("Subtraction", other)

    def mul(self, other: Any) -> Any:
        _ = other
        self._raise_binary("Multiplication", other)

    def div(self, other: Any) -> Any:
        _ = other
        self._raise_binary("Division", other)

    def exp(self, other: Any) -> Any:
        _ = other
        self._raise_binary("Exponentiation", other)


class Int(Val):
    def __init__(self, value: int):
        self.value = int(value)

    def add(self, other: Any):
        if isinstance(other, Num):
            return Num(self.value + other.value)
        elif isinstance(other, Int):
            return Int(self.value + other.value)
        self._raise_binary("Addition", other)

    def sub(self, other: Any):
        if isinstance(other, Num):
            return Num(self.value - other.value)
        elif isinstance(other, Int):
            return Int(self.value - other.value)
        self._raise_binary("Subtraction", other)

    def mul(self, other: Any):
        if isinstance(other, Num):
            return Num(self.value * other.value)
        elif isinstance(other, Int):
            return Int(self.value * other.value)
        self._raise_binary("Multiplication", other)

    def div(self, other: Any):
        if isinstance(other, Num):
            return Num(self.value / other.value)
        elif isinstance(other, Int):
            return Int(self.value / other.value)
        self._raise_binary("Division", other)

    def exp(self, other: Any):
        if isinstance(other, Num):
            return Num(self.value**other.value)
        elif isinstance(other, Int):
            return Int(self.value**other.value)
        self._raise_binary("Exponentiation", other)


class Num(Val):
    def __init__(self, value: float):
        self.value = float(value)
        self._operable = Union[Int, Num]

    def add(self, other: Any):
        if isinstance(other, self._operable):
            return Num(self.value + other.value)
        self._raise_binary("Addition", other)

    def sub(self, other: Any):
        if isinstance(other, self._operable):
            return Num(self.value - other.value)
        self._raise_binary("Subtraction", other)

    def mul(self, other: Any):
        if isinstance(other, self._operable):
            return Num(self.value * other.value)
        self._raise_binary("Multiplication", other)

    def div(self, other: Any):
        if isinstance(other, self._operable):
            return Num(self.value / other.value)
        self._raise_binary("Division", other)

    def exp(self, other: Any):
        if isinstance(other, self._operable):
            return Num(self.value**other.value)
        self._raise_binary("Exponentiation", other)


TYPE_KEYWORDS = {"int": Int, "num": Num}


class Node:
    @staticmethod
    def new_node(node: dict[str, Any] | str, varspace: dict[str, Val]):
        if isinstance(node, str):
            return node
        match node["type"]:
            case "int":
                return IntNode(node, varspace)
            case "num":
                return NumNode(node, varspace)
            case "ident":
                return IdentNode(node, varspace)
            case "atom":
                return AtomNode(node, varspace)
            case "factor":
                return FactorNode(node, varspace)
            case "term":
                return TermNode(node, varspace)
            case "expr":
                return ExprNode(node, varspace)
            case "vardef":
                return VarDefNode(node, varspace)
            case "varset":
                return VarSetNode(node, varspace)
            case "echo":
                return EchoNode(node, varspace)
            case "newline":
                return None
            case _:
                raise ValueError(f"Unsupported node type: {node['type']}\n")


class ValueNode(Node):
    def exec(self) -> Val: ...


class IntNode(ValueNode):
    def __init__(self, node: dict[str, Any], varspace: dict[str, Val]):
        self.value = int(node["children"])
        self.varspace = varspace

    def exec(self):
        return Int(self.value)


class NumNode(ValueNode):
    def __init__(self, node: dict[str, Any], varspace: dict[str, Val]):
        self.value = float(node["children"])
        self.varspace = varspace

    def exec(self):
        return Num(self.value)


class IdentNode(ValueNode):
    def __init__(self, node: dict[str, Any], varspace: dict[str, Val]):
        self.value = node["children"]
        self.varspace = varspace

    def exec(self):
        if self.value in self.varspace:
            return self.varspace[self.value]
        raise SyntaxError(f"Variable {self.value} is not yet defined.\n")


class AtomNode(Node):
    def __init__(self, node: dict[str, Any], varspace: dict[str, Val]):
        self.children = node["children"]
        for ii, child in enumerate(self.children):
            child: dict[str, Any] | Any
            if isinstance(child, dict):
                self.children[ii] = Node.new_node(child, varspace)
        self.col = node["col"]
        self.varspace = varspace
        self.line = node["line"]

    def exec(self) -> Val:
        if not self.children:
            raise SyntaxError(f"Expected Atom at line {self.line}, col {self.col}\n")
        if self.children[0] is literals.L_PAREN:
            if len(self.children) != 3 or self.children[2] != literals.R_PAREN:
                raise SyntaxError(
                    f"Unmatched '(' at line {self.line}, col {self.col}\n"
                )  # )
            value: Any | ExprNode = self.children[1]
            if not isinstance(value, ExprNode):
                raise SyntaxError(
                    f"Expected Expr at line {self.line}, col {self.col}\n"
                )
            return value.exec()
        if len(self.children) > 1:
            raise SyntaxError(
                f"Expected '(' at line {self.line}, col {self.col}\n"
            )  # )

        value = self.children[0]
        if not isinstance(value, ValueNode):
            raise SyntaxError(f"Expected Expr at line {self.line}, col {self.col}\n")
        return value.exec()


class FactorNode(Node):
    def __init__(self, node: dict[str, Any], varspace: dict[str, Val]):
        self.children = node["children"]
        for ii, child in enumerate(self.children):
            child: dict[str, Any] | Any
            self.children[ii] = Node.new_node(child, varspace)
        self.col = node["col"]
        self.varspace = varspace
        self.line = node["line"]

    def exec(self):
        if not self.children:
            raise SyntaxError(f"Expected Factor at line {self.line}, col {self.col}\n")
        if len(self.children) == 1:
            value: Any | AtomNode = self.children[0]
            if not isinstance(value, AtomNode):
                raise SyntaxError(
                    f"Expected Atom at line {self.line}, col {self.col}\n"
                )

            return value.exec()

        op: str | None = None

        right: Any | AtomNode = self.children.pop(0)
        if not isinstance(right, AtomNode):
            raise SyntaxError(f"Expected Atom at line {self.line}, col {self.col}\n")
        right_val: Val = right.exec()

        while self.children:
            if not self.children:
                raise SyntaxError(
                    f"Expected {literals.OP_EXP} at line {self.line}, col {self.col}\n"
                )
            op = self.children.pop(0)
            if op != literals.OP_EXP:
                raise SyntaxError(
                    f"Expected {literals.OP_EXP} at line {self.line}, col {self.col}\n"
                )
            left: Any | AtomNode = self.children.pop(0)
            if not isinstance(left, FactorNode):
                raise SyntaxError(
                    f"Expected Factor at line {self.line}, col {self.col}\n"
                )

            right_val = right_val.exp(left.exec())

        return right_val


class TermNode(Node):
    def __init__(self, node: dict[str, Any], varspace: dict[str, Val]):
        self.children = node["children"]
        for ii, child in enumerate(self.children):
            child: dict[str, Any] | Any
            self.children[ii] = Node.new_node(child, varspace)
        self.col = node["col"]
        self.varspace = varspace
        self.line = node["line"]

    def exec(self):
        if not self.children:
            raise SyntaxError(f"Expected Term at line {self.line}, col {self.col}\n")
        if len(self.children) == 1:
            value: Any | FactorNode = self.children[0]
            if not isinstance(value, FactorNode):
                raise SyntaxError(
                    f"Expected Factor at line {self.line}, col {self.col}\n"
                )

            return value.exec()

        op: str | None = None

        right: Any | FactorNode = self.children.pop(0)
        if not isinstance(right, FactorNode):
            raise SyntaxError(f"Expected Factor at line {self.line}, col {self.col}\n")
        right_val: Val = right.exec()

        while self.children:
            if not self.children:
                raise SyntaxError(
                    f"Expected operator with precidence 2 at line {self.line}, col {self.col}\n"
                )
            op = self.children.pop(0)
            if op not in [literals.OP_MUL, literals.OP_DIV]:
                raise SyntaxError(
                    f"Expected operator with precidence 2 at line {self.line}, col {self.col}\n"
                )
            left: Any | FactorNode = self.children.pop(0)
            if not isinstance(left, FactorNode):
                raise SyntaxError(
                    f"Expected Factor at line {self.line}, col {self.col}\n"
                )
            left_val = left.exec()

            match op:
                case literals.OP_MUL:
                    right_val = right_val.mul(left_val)
                case literals.OP_DIV:
                    right_val = right_val.div(left_val)
                case _:
                    raise SyntaxError(
                        f"Expected operator with precidence 2 at line {self.line}, col {self.col}\n"
                    )

        return right_val


class ExprNode(Node):
    def __init__(self, node: dict[str, Any], varspace: dict[str, Val]):
        self.children = node["children"]
        for ii, child in enumerate(self.children):
            child: dict[str, Any] | Any
            self.children[ii] = Node.new_node(child, varspace)
        self.col = node["col"]
        self.varspace = varspace
        self.line = node["line"]

    def exec(self):
        if not self.children:
            raise SyntaxError(f"Expected Expr at line {self.line}, col {self.col}\n")
        if len(self.children) == 1:
            value: Any | TermNode = self.children[0]
            if not isinstance(value, TermNode):
                raise SyntaxError(
                    f"Expected TermNode at line {self.line}, col {self.col}\n"
                )
            return value.exec()

        op: str | None = None

        right: Any | TermNode = self.children.pop(0)
        if not isinstance(right, TermNode):
            raise SyntaxError(f"Expected Term at line {self.line}, col {self.col}\n")
        right_val: Val = right.exec()

        while self.children:
            if not self.children:
                raise SyntaxError(
                    f"Expected operator with precidence 1 at line {self.line}, col {self.col}\n"
                )
            op = self.children.pop(0)
            if op not in [literals.OP_ADD, literals.OP_SUB]:
                raise SyntaxError(
                    f"Expected operator with precidence 1 at line {self.line}, col {self.col}\n"
                )
            left: Any | TermNode = self.children.pop(0)
            if not isinstance(left, TermNode):
                raise SyntaxError(
                    f"Expected Term at line {self.line}, col {self.col}\n"
                )
            left_val: Val = left.exec()

            match op:
                case literals.OP_ADD:
                    right_val = right_val.add(left_val)
                case literals.OP_SUB:
                    right_val = right_val.sub(left_val)
                case _:
                    raise SyntaxError(
                        f"Expected operator with precidence 2 at line {self.line}, col {self.col}\n"
                    )

        return right_val


class VarDefNode(Node):
    def __init__(self, node: dict[str, Any], varspace: dict[str, Val]):
        self.children = node["children"]
        for ii, child in enumerate(self.children):
            child: dict[str, Any] | Any
            self.children[ii] = Node.new_node(child, varspace)
        self.col = node["col"]
        self.varspace = varspace
        self.line = node["line"]

    def _exec_explicit(self):
        if not isinstance(self.children[0], IdentNode):
            raise SyntaxError(
                f"Invalid variable definition at line {self.line}, col {self.col}\n"
                + "Variable definition must begin with an identifier,\n"
                + "not {self.children[0]}.\n"
            )

        var_name: str = self.children[0].value

        if self.children[1] != ":":
            raise SyntaxError(
                f"Invalid variable definition at line {self.line}, col {self.col}\n"
                + "Expected ':' to specify type in variable definition.\n"
            )

        if not isinstance(self.children[2], IdentNode):
            raise SyntaxError(
                f"Invalid variable definition at line {self.line}, col {self.col}\n"
                + f"Variable type must be with an identifier, not {self.children[0]}.\n"
            )

        try:
            var_type = TYPE_KEYWORDS[self.children[2].value]
        except KeyError:
            raise SyntaxError(
                f"Invalid variable definition at line {self.line}, col {self.col}\n"
                + f"{self.children[2]} is not a valid type.\n"
            )

        if self.children[3] != "=":
            raise SyntaxError(
                f"Invalid variable definition at line {self.line}, col {self.col}\n"
                + "Expected '=' to specify value in variable definition.\n"
            )

        var_val = self.children[4].exec()

        if isinstance(var_val, Val):
            var_val = var_val.value

        try:
            val = var_type(var_val)
        except (TypeError, ValueError):
            raise SyntaxError(
                f"Invalid variable definition at line {self.line}, col {self.col}\n"
                + f"Incompatible value for type {var_type}: {var_val}\n"
            )

        self.varspace[var_name] = val

        return val

    def _exec_implicit(self):
        if not isinstance(self.children[0], IdentNode):
            raise SyntaxError(
                f"Invalid variable definition at line {self.line}, col {self.col}\n"
                + f"Variable definition must begin with an identifier, not {self.children[0]}.\n"
            )

        var_name: str = self.children[0].value

        if self.children[1] != ":":
            raise SyntaxError(
                f"Invalid variable definition at line {self.line}, col {self.col}\n"
                + "Expected ':' to specify type in variable definition.\n"
            )

        if self.children[2] != "=":
            raise SyntaxError(
                f"Invalid variable definition at line {self.line}, col {self.col}\n"
                + "Expected '=' to specify value in variable definition.\n"
            )

        value = self.children[3]

        var_val = value.exec()

        if not isinstance(var_val, Val):
            raise SyntaxError(
                f"Invalid variable definition at line {self.line}, col {self.col}"
                + f"Cannot infer type from '{self.children[3]}'\n"
            )

        self.varspace[var_name] = var_val

        return var_val

    def exec(self):
        if len(self.children) == 5:
            return self._exec_explicit()

        if len(self.children) == 4:
            return self._exec_implicit()

        raise SyntaxError(
            f"Invalid variable definition at line {self.line}, col {self.col}\n"
            + f"Invalid variable definition at col {self.col}\n"
        )


class VarSetNode(Node):
    def __init__(self, node: dict[str, Any], varspace: dict[str, Val]):
        self.children = node["children"]
        for ii, child in enumerate(self.children):
            child: dict[str, Any] | Any
            self.children[ii] = Node.new_node(child, varspace)
        self.col = node["col"]
        self.varspace = varspace
        self.line = node["line"]

    def exec(self):
        if len(self.children) != 3:
            raise SyntaxError(
                f"Invalid variable reset at line {self.line}, col {self.col}\n"
                + f"Invalid variable definition at col {self.col}\n"
            )

        if not isinstance(self.children[0], IdentNode):
            raise SyntaxError(
                f"Invalid variable reset at line {self.line}, col {self.col}\n"
                + f"Variable reset must begin with an identifier, not {self.children[0]}.\n"
            )

        var_name: str = self.children[0].value

        if var_name not in self.varspace:
            raise SyntaxError(
                f"Invalid variable reset at line {self.line}, col {self.col}\n"
                + "Can only reset variable reset it's been defined.\n"
                + f"{var_name} has not yet been defined.\n"
            )

        var_type = type(self.varspace[var_name])

        if self.children[1] != "=":
            raise SyntaxError(
                f"Invalid variable reset at line {self.line}, col {self.col}\n"
                + "Expected '=' to specify value in variable reset.\n"
            )

        var_val = self.children[2].exec()

        val = var_type(var_val.value)

        self.varspace[var_name] = val

        return val


class EchoNode(Node):
    def __init__(self, node: dict[str, Any], varspace: dict[str, Val]):
        self.children = node["children"]
        for ii, child in enumerate(self.children):
            child: dict[str, Any] | Any
            self.children[ii] = Node.new_node(child, varspace)
        self.col = node["col"]
        self.varspace = varspace
        self.line = node["line"]

    def exec(self):
        if len(self.children) != 2:
            raise SyntaxError(
                f"Invalid echo statement at line {self.line}, col {self.col}"
            )

        if not isinstance(self.children[1], ExprNode):
            raise SyntaxError(f"Expected Expr at line {self.line}, col {self.col}")

        expr = self.children[1].exec()

        print(expr, flush=True)

        return expr


class Executor:
    def __init__(self):
        self.globals: dict[str, Val] = {}

    def exec(self, ast: list[dict[str, Any]]):
        statements: list[Any] = []
        for ast_node in ast:
            node = Node.new_node(ast_node, self.globals)
            if isinstance(node, str):
                raise SyntaxError(f"{node} cannot be executed.")
            if node is not None:
                statements.append(node.exec())

        if not statements:
            return None

        return statements[-1]

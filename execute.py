"""Module providing the interpreter"""

import enum
from typing import Any

import literals


class Types(enum.Enum):
    INT = "int"
    NUM = "num"


class Var:
    def __init__(self, val_type: Types, val: Any):
        self.type = val_type
        match val_type:
            case Types.INT:
                try:
                    self.value = int(val)
                except ValueError:
                    raise SyntaxError(f"{val} is not a valid int.")

            case Types.NUM:
                try:
                    self.value = float(val)
                except ValueError:
                    raise SyntaxError(f"{val} is not a valid num.")


class Node:
    @staticmethod
    def new_node(node: dict[str, Any] | str, varspace: dict[str, Var]):
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
            case _:
                raise ValueError(f"Unsupported node type: {node['type']}")


class IntNode(Node):
    def __init__(self, node: dict[str, Any], varspace: dict[str, Var]):
        self.value = int(node["children"])
        self.varspace = varspace

    def exec(self):
        return self.value


class NumNode(Node):
    def __init__(self, node: dict[str, Any], varspace: dict[str, Var]):
        self.value = float(node["children"])
        self.varspace = varspace

    def exec(self):
        return self.value


class IdentNode(Node):
    def __init__(self, node: dict[str, Any], varspace: dict[str, Var]):
        self.value = node["children"]
        self.varspace = varspace

    def exec(self):
        if self.value in self.varspace:
            return self.varspace[self.value].value
        raise SyntaxError(f"Variable {self.value} is not yet defined.")


class AtomNode(Node):
    def __init__(self, node: dict[str, Any], varspace: dict[str, Var]):
        self.children = node["children"]
        for ii, child in enumerate(self.children):
            child: dict[str, Any] | Any
            if isinstance(child, dict):
                self.children[ii] = Node.new_node(child, varspace)
        self.col = node["col"]
        self.varspace = varspace

    def exec(self):
        if not self.children:
            raise SyntaxError(f"Expected Atom at col {self.col}")
        if self.children[0] is literals.L_PAREN:
            if len(self.children) != 3 or self.children[2] != literals.R_PAREN:
                raise SyntaxError(f"Unmatched '(' at col {self.col}")  # )
            if not isinstance(self.children[1], Node):
                raise SyntaxError(f"Expected Expr at col {self.col}")
            return self.children[1].exec()
        if len(self.children) > 1:
            raise SyntaxError(f"Expected '(' at col {self.col}")  # )
        return self.children[0].exec()


class FactorNode(Node):
    def __init__(self, node: dict[str, Any], varspace: dict[str, Var]):
        self.children = node["children"]
        for ii, child in enumerate(self.children):
            child: dict[str, Any] | Any
            self.children[ii] = Node.new_node(child, varspace)
        self.col = node["col"]
        self.varspace = varspace

    def exec(self):
        if not self.children:
            raise SyntaxError(f"Expected Factor at col {self.col}")
        if len(self.children) == 1:
            return self.children[0].exec()

        right: Any
        left: Any
        op: str | None = None

        right = self.children.pop(0)
        if not isinstance(right, AtomNode):
            raise SyntaxError(f"Expected Atom at col {self.col}")
        right = right.exec()

        while self.children:
            if not self.children:
                raise SyntaxError(f"Expected {literals.OP_EXP} at col {self.col}")
            op = self.children.pop(0)
            if op != literals.OP_EXP:
                raise SyntaxError(f"Expected {literals.OP_EXP} at col {self.col}")
            left = self.children.pop(0)
            if not isinstance(left, FactorNode):
                raise SyntaxError(f"Expected Factor at col {self.col}")
            left = left.exec()

            right = right**left

        return right


class TermNode(Node):
    def __init__(self, node: dict[str, Any], varspace: dict[str, Var]):
        self.children = node["children"]
        for ii, child in enumerate(self.children):
            child: dict[str, Any] | Any
            self.children[ii] = Node.new_node(child, varspace)
        self.col = node["col"]
        self.varspace = varspace

    def exec(self):
        if not self.children:
            raise SyntaxError(f"Expected Term at col {self.col}")
        if len(self.children) == 1:
            return self.children[0].exec()

        right: Any
        left: Any
        op: str | None = None

        right = self.children.pop(0)
        if not isinstance(right, FactorNode):
            raise SyntaxError(f"Expected Factor at col {self.col}")
        right = right.exec()

        while self.children:
            if not self.children:
                raise SyntaxError(
                    f"Expected operator with precidence 2 at col {self.col}"
                )
            op = self.children.pop(0)
            if op not in [literals.OP_MUL, literals.OP_DIV]:
                raise SyntaxError(
                    f"Expected operator with precidence 2 at col {self.col}"
                )
            left = self.children.pop(0)
            if not isinstance(left, FactorNode):
                raise SyntaxError(f"Expected Term at col {self.col}")
            left = left.exec()

            match op:
                case literals.OP_MUL:
                    right = right * left
                case literals.OP_DIV:
                    right = right / left
                case _:
                    raise SyntaxError(
                        f"Expected operator with precidence 2 at col {self.col}"
                    )

        return right


class ExprNode(Node):
    def __init__(self, node: dict[str, Any], varspace: dict[str, Var]):
        self.children = node["children"]
        for ii, child in enumerate(self.children):
            child: dict[str, Any] | Any
            self.children[ii] = Node.new_node(child, varspace)
        self.col = node["col"]
        self.varspace = varspace

    def exec(self):
        if not self.children:
            raise SyntaxError(f"Expected Expr at col {self.col}")
        if len(self.children) == 1:
            return self.children[0].exec()

        right: Any
        left: Any
        op: str | None = None

        right = self.children.pop(0)
        if not isinstance(right, TermNode):
            raise SyntaxError(f"Expected Term at col {self.col}")
        right = right.exec()

        while self.children:
            if not self.children:
                raise SyntaxError(
                    f"Expected operator with precidence 1 at col {self.col}"
                )
            op = self.children.pop(0)
            if op not in [literals.OP_ADD, literals.OP_SUB]:
                raise SyntaxError(
                    f"Expected operator with precidence 1 at col {self.col}"
                )
            left = self.children.pop(0)
            if not isinstance(left, TermNode):
                raise SyntaxError(f"Expected Term at col {self.col}")
            left = left.exec()

            match op:
                case literals.OP_ADD:
                    right = right + left
                case literals.OP_SUB:
                    right = right - left
                case _:
                    raise SyntaxError(
                        f"Expected operator with precidence 2 at col {self.col}"
                    )

        return right


class VarDefNode(Node):
    def __init__(self, node: dict[str, Any], varspace: dict[str, Var]):
        self.children = node["children"]
        for ii, child in enumerate(self.children):
            child: dict[str, Any] | Any
            self.children[ii] = Node.new_node(child, varspace)
        self.col = node["col"]
        self.varspace = varspace

    def exec(self):
        if len(self.children) != 5:
            raise SyntaxError(f"Invalid variable definition at col {self.col}")

        if not isinstance(self.children[0], IdentNode):
            raise SyntaxError(
                f"Variable definition must begin with an identifier, not {self.children[0]}."
            )

        var_name: str = self.children[0].value

        if self.children[1] != ":":
            raise SyntaxError("Expected ':' to specify type in variable definition.")

        if not isinstance(self.children[2], IdentNode):
            raise SyntaxError(
                f"Variable type must be with an identifier, not {self.children[0]}."
            )

        try:
            var_type = Types(self.children[2].value)
        except ValueError:
            raise SyntaxError(f"{self.children[2]} is not a valid type.")

        if self.children[3] != "=":
            raise SyntaxError("Expected '=' to specify value in variable definition.")

        var_val = self.children[4].exec()

        var = Var(var_type, var_val)

        self.varspace[var_name] = var

        return var.value


class VarSetNode(Node):
    def __init__(self, node: dict[str, Any], varspace: dict[str, Var]):
        self.children = node["children"]
        for ii, child in enumerate(self.children):
            child: dict[str, Any] | Any
            self.children[ii] = Node.new_node(child, varspace)
        self.col = node["col"]
        self.varspace = varspace

    def exec(self):
        if len(self.children) != 3:
            raise SyntaxError(f"Invalid variable definition at col {self.col}")

        if not isinstance(self.children[0], IdentNode):
            raise SyntaxError(
                f"Variable reset must begin with an identifier, not {self.children[0]}."
            )

        var_name: str = self.children[0].value

        if var_name not in self.varspace:
            raise SyntaxError(
                "Can only reset variable after it's been defined.\n"
                + f"{var_name} has not yet been defined."
            )

        var_type = self.varspace[var_name].type

        if self.children[1] != "=":
            raise SyntaxError("Expected '=' to specify value in variable reset.")

        var_val = self.children[2].exec()

        var = Var(var_type, var_val)

        self.varspace[var_name] = var

        return var.value


class Executor:
    def __init__(self):
        self.globals: dict[str, Var] = {}

    def exec(self, ast: dict[str, Any]):
        node = Node.new_node(ast, self.globals)
        if isinstance(node, str):
            return node
        return node.exec()

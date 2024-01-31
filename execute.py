"""Module providing the interpreter"""

from typing import Any

import literals


class Node:
    @staticmethod
    def new_node(node: dict[str, Any] | str):
        if isinstance(node, str):
            return node
        match node["type"]:
            case "int":
                return IntNode(node)
            case "num":
                return NumNode(node)
            case "ident":
                return IdentNode(node)
            case "atom":
                return AtomNode(node)
            case "factor":
                return FactorNode(node)
            case "term":
                return TermNode(node)
            case "expr":
                return ExprNode(node)
            case _:
                raise ValueError(f"Unsupported node type: {node['type']}")


class IntNode(Node):
    def __init__(self, node: dict[str, Any]):
        self.value = int(node["children"])

    def exec(self):
        return self.value


class NumNode(Node):
    def __init__(self, node: dict[str, Any]):
        self.value = float(node["children"])

    def exec(self):
        return self.value


class IdentNode(Node):
    def __init__(self, node: dict[str, Any]):
        self.value = node["children"]

    def exec(self):
        return self.value


class AtomNode(Node):
    def __init__(self, node: dict[str, Any]):
        self.children = node["children"]
        for ii, child in enumerate(self.children):
            child: dict[str, Any] | Any
            if isinstance(child, dict):
                self.children[ii] = Node.new_node(child)
        self.col = node["col"]

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
    def __init__(self, node: dict[str, Any]):
        self.children = node["children"]
        for ii, child in enumerate(self.children):
            child: dict[str, Any] | Any
            self.children[ii] = Node.new_node(child)
        self.col = node["col"]

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
    def __init__(self, node: dict[str, Any]):
        self.children = node["children"]
        for ii, child in enumerate(self.children):
            child: dict[str, Any] | Any
            self.children[ii] = Node.new_node(child)
        self.col = node["col"]

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
    def __init__(self, node: dict[str, Any]):
        self.children = node["children"]
        for ii, child in enumerate(self.children):
            child: dict[str, Any] | Any
            self.children[ii] = Node.new_node(child)
        self.col = node["col"]

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


class Executor:
    def __init__(self):
        self.globals: dict[str, Any] = {}

    def exec(self, ast: dict[str, Any]):
        node = Node.new_node(ast)
        if isinstance(node, str):
            return node
        return node.exec()

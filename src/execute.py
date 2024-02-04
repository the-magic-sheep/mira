"""Module providing the interpreter"""

import copy
from typing import Any, Type, Union

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


class CallableType:
    def __init__(self, return_type: Type[Val], params: dict[str, Type[Val]]):
        self.params = params
        self.return_type = return_type


class Callable:
    def __init__(self, name: str, callable_type: CallableType, definition: "ExprNode"):
        self.name = name
        self.type = callable_type
        self.definition = definition

    def call(self, params: dict[str, Val]):

        definition = copy.deepcopy(self.definition)

        if set(params) - set(self.type.params):
            extra_params = ""
            for param in set(params) - set(self.type.params):
                extra_params += param + ", "

            extra_params = extra_params[:-2]
            raise SyntaxError(
                f"Callable 'f{self.name}' recieved unexpected paramuments:\n"
                + extra_params
            )

        if set(self.type.params) - set(params):
            missing_params = ""
            for param in set(self.type.params) - set(params):
                missing_params += param + ", "

            missing_params = missing_params[:-2]
            raise SyntaxError(
                f"Callable 'f{self.name}' missing paramuments:\n" + missing_params
            )

        for param_name, param_val in params.items():
            definition.varspace[param_name] = param_val

        return self.type.return_type(definition.exec().value)


TYPE_KEYWORDS = {"int": Int, "num": Num}


class Node:
    @staticmethod
    def new_node(
        node: dict[str, Any] | str,
        varspace: dict[str, Val],
        callspace: dict[str, Callable],
    ):
        if isinstance(node, str):
            return node
        match node["type"]:
            case "int":
                return IntNode(node, varspace, callspace)
            case "num":
                return NumNode(node, varspace, callspace)
            case "ident":
                return IdentNode(node, varspace, callspace)
            case "atom":
                return AtomNode(node, varspace, callspace)
            case "factor":
                return FactorNode(node, varspace, callspace)
            case "term":
                return TermNode(node, varspace, callspace)
            case "expr":
                return ExprNode(node, varspace, callspace)
            case "vardef":
                return VarDefNode(node, varspace, callspace)
            case "varset":
                return VarSetNode(node, varspace, callspace)
            case "echo":
                return EchoNode(node, varspace, callspace)
            case "newline":
                return None
            case "paramlist":
                return ParamListNode(node, varspace, callspace)
            case "callable":
                return CallableNode(node, varspace, callspace)
            case "callable_def":
                return CallableDefNode(node, varspace, callspace)
            case "arglist":
                return ArgListNode(node, varspace, callspace)
            case "call":
                return CallNode(node, varspace, callspace)
            case _:
                raise ValueError(f"Unsupported node type: {node['type']}\n")


class ValueNode(Node):
    def exec(self) -> Val: ...


class IntNode(ValueNode):
    def __init__(
        self,
        node: dict[str, Any],
        varspace: dict[str, Val],
        callspace: dict[str, Callable],
    ):
        self.value = int(node["children"])
        self.varspace = varspace
        self.callspace = callspace

    def exec(self):
        return Int(self.value)


class NumNode(ValueNode):
    def __init__(
        self,
        node: dict[str, Any],
        varspace: dict[str, Val],
        callspace: dict[str, Callable],
    ):
        self.value = float(node["children"])
        self.varspace = varspace
        self.callspace = callspace

    def exec(self):
        return Num(self.value)


class IdentNode(ValueNode):
    def __init__(
        self,
        node: dict[str, Any],
        varspace: dict[str, Val],
        callspace: dict[str, Callable],
    ):
        self.value: str = node["children"]
        self.varspace = varspace
        self.callspace = callspace

    def exec(self):
        if self.value in self.varspace:
            return self.varspace[self.value]
        raise SyntaxError(f"Variable {self.value} is not yet defined.\n")


class ArgListNode(Node):
    def __init__(
        self,
        node: dict[str, Any],
        varspace: dict[str, Val],
        callspace: dict[str, Callable],
    ):
        self.children = node["children"]
        for ii, child in enumerate(self.children):
            child: dict[str, Any] | Any
            if isinstance(child, dict):
                self.children[ii] = Node.new_node(child, varspace, callspace)
        self.col = node["col"]
        self.varspace = varspace
        self.callspace = callspace
        self.line = node["line"]

    def exec(self):

        args: dict[str, Val] = {}
        children = self.children.copy()
        while children:
            ident = children.pop(0)
            if not isinstance(ident, IdentNode):
                raise SyntaxError(
                    f"Invalid arglist at line {self.line}, col {self.col}.\n"
                    + "Expected identifier."
                )

            arg_ident = ident.value

            if arg_ident in args:
                raise SyntaxError(
                    f"Invalid arglist at line {self.line}, col {self.col}.\n"
                    + f"Argument {arg_ident} is repeated."
                )

            # Consume '='
            children.pop(0)

            arg_expr = children.pop(0)
            if not isinstance(arg_expr, ExprNode):
                raise SyntaxError(
                    f"Invalid arglist at line {self.line}, col {self.col}.\n"
                    + "Expected expression."
                )

            arg_val = arg_expr.exec()

            args[arg_ident] = arg_val

            if children:
                # Pop the optional comma
                children.pop(0)

        return args


class CallNode(ValueNode):
    def __init__(
        self,
        node: dict[str, Any],
        varspace: dict[str, Val],
        callspace: dict[str, Callable],
    ):
        self.children = node["children"]
        for ii, child in enumerate(self.children):
            child: dict[str, Any] | Any
            if isinstance(child, dict):
                self.children[ii] = Node.new_node(child, varspace, callspace)
        self.col = node["col"]
        self.varspace = varspace
        self.callspace = callspace
        self.line = node["line"]

    def exec(self):
        callable_ident = self.children[0]
        if not isinstance(callable_ident, IdentNode):
            raise SyntaxError(
                f"Invalid call at line {self.line}, col {self.col}.\n"
                + "Expected identifier."
            )
        callable_name = callable_ident.value

        if callable_name not in self.callspace:
            raise SyntaxError(
                f"Invalid call at line {self.line}, col {self.col}."
                + f"callable {callable_name} has not yet been defined."
            )

        arglist: ArgListNode = self.children[2]

        args = arglist.exec()

        try:
            return self.callspace[callable_name].call(args)
        except RecursionError:
            raise SyntaxError(
                "Maximum recursion depth reached during call.\n"
                + f"In call '{callable_name}' at line {self.line}, col {self.col}."
            )


class ParamListNode(Node):
    def __init__(
        self,
        node: dict[str, Any],
        varspace: dict[str, Val],
        callspace: dict[str, Callable],
    ):
        self.children = node["children"]
        for ii, child in enumerate(self.children):
            child: dict[str, Any] | Any
            if isinstance(child, dict):
                self.children[ii] = Node.new_node(child, varspace, callspace)
        self.col = node["col"]
        self.varspace = varspace
        self.callspace = callspace
        self.line = node["line"]

    def exec(self):

        params: dict[str, Type[Val]] = {}
        children = self.children.copy()
        while children:
            ident = children.pop(0)
            if not isinstance(ident, IdentNode):
                raise SyntaxError(
                    f"Invalid paramlist at line {self.line}, col {self.col}."
                    + "Expected identifier."
                )

            param_ident = ident.value

            if param_ident in params:
                raise SyntaxError(
                    f"Invalid paramlist at line {self.line}, col {self.col}."
                    + f"Parameter {param_ident} is repeated."
                )

            # Consume ':'
            children.pop(0)

            param_type = children.pop(0)
            if not isinstance(param_type, IdentNode):
                raise SyntaxError(
                    f"Invalid paramlist at line {self.line}, col {self.col}."
                    + "Expected identifier."
                )

            if param_type.value not in TYPE_KEYWORDS:
                raise SyntaxError(
                    f"Invalid paramlist at line {self.line}, col {self.col}."
                    + f"{param_type.value} is not a valid type."
                )

            params[param_ident] = TYPE_KEYWORDS[param_type.value]

            if children:
                # Pop the optional comma
                children.pop(0)

        return params


class CallableNode(Node):
    def __init__(
        self,
        node: dict[str, Any],
        varspace: dict[str, Val],
        callspace: dict[str, Callable],
    ):
        self.children = node["children"]
        for ii, child in enumerate(self.children):
            child: dict[str, Any] | Any
            if isinstance(child, dict):
                self.children[ii] = Node.new_node(child, varspace, callspace)
        self.col = node["col"]
        self.varspace = varspace
        self.callspace = callspace
        self.line = node["line"]

    def exec(self):
        return_type_ident: IdentNode = self.children.pop(0)

        return_type = return_type_ident.value

        if return_type not in TYPE_KEYWORDS:
            raise SyntaxError(
                f"Invalid callable type at line {self.line}, col {self.col}\n"
                + f"{return_type} is not a valid return type."
            )

        self.children.pop(0)

        if self.children[0] == ")":
            return CallableType(TYPE_KEYWORDS[return_type], {})

        paramlist: ParamListNode = self.children[0]

        return CallableType(TYPE_KEYWORDS[return_type], paramlist.exec())


class CallableDefNode(Node):
    def __init__(
        self,
        node: dict[str, Any],
        varspace: dict[str, Val],
        callspace: dict[str, Callable],
    ):
        self.children = node["children"]
        for ii, child in enumerate(self.children):
            child: dict[str, Any] | Any
            if isinstance(child, dict):
                self.children[ii] = Node.new_node(child, varspace, callspace)
        self.col = node["col"]
        self.varspace = varspace
        self.callspace = callspace
        self.line = node["line"]

    def exec(self):
        callable_name: str = self.children[0].value

        callable_type: CallableType = self.children[2].exec()

        expr: ExprNode = self.children[4]

        callable_ = Callable(callable_name, callable_type, expr)
        self.callspace[callable_name] = callable_
        if callable_name in self.varspace:
            del self.varspace[callable_name]

        return callable_


class AtomNode(Node):
    def __init__(
        self,
        node: dict[str, Any],
        varspace: dict[str, Val],
        callspace: dict[str, Callable],
    ):
        self.children = node["children"]
        self.col = node["col"]
        self.varspace = varspace
        self.callspace = callspace
        self.line = node["line"]

    def exec(self) -> Val:
        children = [
            Node.new_node(child, self.varspace, self.callspace)
            for child in self.children
        ]
        if not children:
            raise SyntaxError(f"Expected Atom at line {self.line}, col {self.col}\n")
        if children[0] is literals.L_PAREN:
            if len(children) != 3 or children[2] != literals.R_PAREN:
                raise SyntaxError(
                    f"Unmatched '(' at line {self.line}, col {self.col}\n"
                )  # )
            value: Any | ExprNode = children[1]
            if not isinstance(value, ExprNode):
                raise SyntaxError(
                    f"Expected Expr at line {self.line}, col {self.col}\n"
                )
            return value.exec()
        if len(children) > 1:
            raise SyntaxError(
                f"Expected '(' at line {self.line}, col {self.col}\n"
            )  # )

        value = children[0]
        if not isinstance(value, ValueNode):
            raise SyntaxError(f"Expected value at line {self.line}, col {self.col}\n")
        return value.exec()


class FactorNode(Node):
    def __init__(
        self,
        node: dict[str, Any],
        varspace: dict[str, Val],
        callspace: dict[str, Callable],
    ):
        self.children = node["children"]
        self.col = node["col"]
        self.varspace = varspace
        self.callspace = callspace
        self.line = node["line"]

    def exec(self):
        children = [
            Node.new_node(child, self.varspace, self.callspace)
            for child in self.children
        ]
        if not children:
            raise SyntaxError(f"Expected Factor at line {self.line}, col {self.col}\n")
        if len(children) == 1:
            value: Any | AtomNode = children[0]
            if not isinstance(value, AtomNode):
                raise SyntaxError(
                    f"Expected Atom at line {self.line}, col {self.col}\n"
                )

            return value.exec()

        op: Any | None = None

        right: Any | AtomNode = children.pop(0)
        if not isinstance(right, AtomNode):
            raise SyntaxError(f"Expected Atom at line {self.line}, col {self.col}\n")
        right_val: Val = right.exec()

        while children:
            if not children:
                raise SyntaxError(
                    f"Expected {literals.OP_EXP} at line {self.line}, col {self.col}\n"
                )
            op = children.pop(0)
            if op != literals.OP_EXP:
                raise SyntaxError(
                    f"Expected {literals.OP_EXP} at line {self.line}, col {self.col}\n"
                )
            left: Any | AtomNode = children.pop(0)
            if not isinstance(left, FactorNode):
                raise SyntaxError(
                    f"Expected Factor at line {self.line}, col {self.col}\n"
                )

            right_val = right_val.exp(left.exec())

        return right_val


class TermNode(Node):
    def __init__(
        self,
        node: dict[str, Any],
        varspace: dict[str, Val],
        callspace: dict[str, Callable],
    ):
        self.children = node["children"]
        self.col = node["col"]
        self.varspace = varspace
        self.callspace = callspace
        self.line = node["line"]

    def exec(self):
        children = [
            Node.new_node(child, self.varspace, self.callspace)
            for child in self.children
        ]
        if not children:
            raise SyntaxError(f"Expected Term at line {self.line}, col {self.col}\n")
        if len(children) == 1:
            value: Any | FactorNode = children[0]
            if not isinstance(value, FactorNode):
                raise SyntaxError(
                    f"Expected Factor at line {self.line}, col {self.col}\n"
                )

            return value.exec()

        op: Any | None = None

        right: Any | FactorNode = children.pop(0)
        if not isinstance(right, FactorNode):
            raise SyntaxError(f"Expected Factor at line {self.line}, col {self.col}\n")
        right_val: Val = right.exec()

        while children:
            if not children:
                raise SyntaxError(
                    f"Expected operator with precidence 2 at line {self.line}, col {self.col}\n"
                )
            op = children.pop(0)
            if op not in [literals.OP_MUL, literals.OP_DIV]:
                raise SyntaxError(
                    f"Expected operator with precidence 2 at line {self.line}, col {self.col}\n"
                )
            left: Any | FactorNode = children.pop(0)
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
    def __init__(
        self,
        node: dict[str, Any],
        varspace: dict[str, Val],
        callspace: dict[str, Callable],
    ):
        self.children = node["children"]
        self.col = node["col"]
        self.varspace = varspace
        self.callspace = callspace
        self.line = node["line"]

    def exec(self):
        children = [
            Node.new_node(child, self.varspace, self.callspace)
            for child in self.children
        ]
        if not children:
            raise SyntaxError(f"Expected Expr at line {self.line}, col {self.col}\n")
        if len(children) == 1:
            value: Any | TermNode = children[0]
            if not isinstance(value, TermNode):
                raise SyntaxError(
                    f"Expected TermNode at line {self.line}, col {self.col}\n"
                )
            return value.exec()

        op: Any | None = None

        right: Any | TermNode = children.pop(0)
        if not isinstance(right, TermNode):
            raise SyntaxError(f"Expected Term at line {self.line}, col {self.col}\n")
        right_val: Val = right.exec()

        while children:
            if not children:
                raise SyntaxError(
                    f"Expected operator with precidence 1 at line {self.line}, col {self.col}\n"
                )
            op = children.pop(0)
            if op not in [literals.OP_ADD, literals.OP_SUB]:
                raise SyntaxError(
                    f"Expected operator with precidence 1 at line {self.line}, col {self.col}\n"
                )
            left: Any | TermNode = children.pop(0)
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
    def __init__(
        self,
        node: dict[str, Any],
        varspace: dict[str, Val],
        callspace: dict[str, Callable],
    ):
        self.children = node["children"]
        for ii, child in enumerate(self.children):
            child: dict[str, Any] | Any
            self.children[ii] = Node.new_node(child, varspace, callspace)
        self.col = node["col"]
        self.varspace = varspace
        self.callspace = callspace
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
        if var_name in self.callspace:
            del self.callspace[var_name]

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
        if var_name in self.callspace:
            del self.callspace[var_name]

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
    def __init__(
        self,
        node: dict[str, Any],
        varspace: dict[str, Val],
        callspace: dict[str, Callable],
    ):
        self.children = node["children"]
        for ii, child in enumerate(self.children):
            child: dict[str, Any] | Any
            self.children[ii] = Node.new_node(child, varspace, callspace)
        self.col = node["col"]
        self.varspace = varspace
        self.callspace = callspace
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
    def __init__(
        self,
        node: dict[str, Any],
        varspace: dict[str, Val],
        callspace: dict[str, Callable],
    ):
        self.children = node["children"]
        for ii, child in enumerate(self.children):
            child: dict[str, Any] | Any
            self.children[ii] = Node.new_node(child, varspace, callspace)
        self.col = node["col"]
        self.varspace = varspace
        self.callspace = callspace
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
        self.callables: dict[str, Callable] = {}

    def exec(self, ast: list[dict[str, Any]]):
        rv = None
        for ast_node in ast:
            node = Node.new_node(ast_node, self.globals, self.callables)
            if isinstance(node, str):
                raise SyntaxError(f"{node} cannot be executed.")
            if node is not None:
                rv = node.exec()

        return rv

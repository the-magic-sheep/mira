"""
This type stub file was generated by pyright.
"""

import typing
from .util import replaced_by_pep8
from .unicode import pyparsing_unicode as ppu

class ExceptionWordUnicode(ppu.Latin1, ppu.LatinA, ppu.LatinB, ppu.Greek, ppu.Cyrillic):
    ...


_extract_alphanums = ...
_exception_word_extractor = ...
class ParseBaseException(Exception):
    """base exception class for all parsing runtime exceptions"""
    loc: int
    msg: str
    pstr: str
    parser_element: typing.Any
    args: typing.Tuple[str, int, typing.Optional[str]]
    __slots__ = ...
    def __init__(self, pstr: str, loc: int = ..., msg: typing.Optional[str] = ..., elem=...) -> None:
        ...
    
    @staticmethod
    def explain_exception(exc, depth=...): # -> LiteralString:
        """
        Method to take an exception and translate the Python internal traceback into a list
        of the pyparsing expressions that caused the exception to be raised.

        Parameters:

        - exc - exception raised during parsing (need not be a ParseException, in support
          of Python exceptions that might be raised in a parse action)
        - depth (default=16) - number of levels back in the stack trace to list expression
          and function names; if None, the full stack trace names will be listed; if 0, only
          the failing input line, marker, and exception string will be shown

        Returns a multi-line string listing the ParserElements and/or function names in the
        exception's stack trace.
        """
        ...
    
    @property
    def line(self) -> str:
        """
        Return the line of text where the exception occurred.
        """
        ...
    
    @property
    def lineno(self) -> int:
        """
        Return the 1-based line number of text where the exception occurred.
        """
        ...
    
    @property
    def col(self) -> int:
        """
        Return the 1-based column on the line of text where the exception occurred.
        """
        ...
    
    @property
    def column(self) -> int:
        """
        Return the 1-based column on the line of text where the exception occurred.
        """
        ...
    
    @property
    def parserElement(self): # -> Any:
        ...
    
    @parserElement.setter
    def parserElement(self, elem): # -> None:
        ...
    
    def __str__(self) -> str:
        ...
    
    def __repr__(self): # -> str:
        ...
    
    def mark_input_line(self, marker_string: typing.Optional[str] = ..., *, markerString: str = ...) -> str:
        """
        Extracts the exception line from the input string, and marks
        the location of the exception with a special symbol.
        """
        ...
    
    def explain(self, depth=...) -> str:
        """
        Method to translate the Python internal traceback into a list
        of the pyparsing expressions that caused the exception to be raised.

        Parameters:

        - depth (default=16) - number of levels back in the stack trace to list expression
          and function names; if None, the full stack trace names will be listed; if 0, only
          the failing input line, marker, and exception string will be shown

        Returns a multi-line string listing the ParserElements and/or function names in the
        exception's stack trace.

        Example::

            expr = pp.Word(pp.nums) * 3
            try:
                expr.parse_string("123 456 A789")
            except pp.ParseException as pe:
                print(pe.explain(depth=0))

        prints::

            123 456 A789
                    ^
            ParseException: Expected W:(0-9), found 'A'  (at char 8), (line:1, col:9)

        Note: the diagnostic output will include string representations of the expressions
        that failed to parse. These representations will be more helpful if you use `set_name` to
        give identifiable names to your expressions. Otherwise they will use the default string
        forms, which may be cryptic to read.

        Note: pyparsing's default truncation of exception tracebacks may also truncate the
        stack of expressions that are displayed in the ``explain`` output. To get the full listing
        of parser expressions, you may have to set ``ParserElement.verbose_stacktrace = True``
        """
        ...
    
    @replaced_by_pep8(mark_input_line)
    def markInputline(self): # -> None:
        ...
    


class ParseException(ParseBaseException):
    """
    Exception thrown when a parse expression doesn't match the input string

    Example::

        try:
            Word(nums).set_name("integer").parse_string("ABC")
        except ParseException as pe:
            print(pe)
            print("column: {}".format(pe.column))

    prints::

       Expected integer (at char 0), (line:1, col:1)
        column: 1

    """
    ...


class ParseFatalException(ParseBaseException):
    """
    User-throwable exception thrown when inconsistent parse content
    is found; stops all parsing immediately
    """
    ...


class ParseSyntaxException(ParseFatalException):
    """
    Just like :class:`ParseFatalException`, but thrown internally
    when an :class:`ErrorStop<And._ErrorStop>` ('-' operator) indicates
    that parsing is to stop immediately because an unbacktrackable
    syntax error has been found.
    """
    ...


class RecursiveGrammarException(Exception):
    """
    Exception thrown by :class:`ParserElement.validate` if the
    grammar could be left-recursive; parser may need to enable
    left recursion using :class:`ParserElement.enable_left_recursion<ParserElement.enable_left_recursion>`
    """
    def __init__(self, parseElementList) -> None:
        ...
    
    def __str__(self) -> str:
        ...
    



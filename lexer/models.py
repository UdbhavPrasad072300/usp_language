from enum import Enum

from pydantic import BaseModel


class Keywords(Enum):
    IF = 'if'
    THEN = 'then'
    ELSE = 'else'
    END = 'end'
    WHILE = 'while'
    DO = 'do'
    FOR = 'for'
    TO = 'to'
    STEP = 'step'
    PRINT = 'print'
    RETURN = 'return'


class Operators(Enum):
    PLUS = '+'
    MINUS = '-'
    TIMES = '*'
    DIVIDE = '/'
    EQUALS = '='
    NOT_EQUALS = '<>'
    LESS_THAN = '<'
    LESS_THAN_OR_EQUALS = '<='
    GREATER_THAN = '>'


class Separator(Enum):
    COMMA = ','
    SEMICOLON = ';'
    COLON = ':'
    DOT = '.'
    LPAREN = '('
    RPAREN = ')'
    LBRACE = '{'
    RBRACE = '}'
    LBRACKET = '['


class Literal(Enum):
    STRING = 'STRING'
    INTEGER = 'INTEGER'


class String(Enum):
    SINGLE_QUOTE = '\''
    DOUBLE_QUOTE = '"'


class Comment(Enum):
    Com = '#'


class Whitespace(Enum):
    SPACE = ' '
    TAB = '\t'
    NEWLINE = '\n'


class TokenType(Enum):
    """
    https://en.wikipedia.org/wiki/Lexical_analysis
    """

    IDENTIFIER = 1
    KEYWORD = 2
    SEPARATOR = 3
    OPERATOR = 4
    LITERAL = 5
    COMMENT = 6
    WHITESPACE = 7


class Token(BaseModel):
    type: TokenType
    value: str = ''

    def __str__(self):
        return f'Token(type={self.type.name}, value={self.value})'

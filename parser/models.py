from typing import List, Any
from enum import Enum

from pydantic import BaseModel

from lexer.models import Token


class ASTNodeType(Enum):
    PROGRAM = "PROGRAM"
    VARIABLE_DECLARATION = "VARIABLE_DECLARATION"
    VARIABLE_ASSIGNMENT = "VARIABLE_ASSIGNMENT"
    IF_STATEMENT = "IF_STATEMENT"
    WHILE_STATEMENT = "WHILE_STATEMENT"
    FOR_STATEMENT = "FOR_STATEMENT"
    FUNCTION_DECLARATION = "FUNCTION_DECLARATION"
    FUNCTION_CALL = "FUNCTION_CALL"
    RETURN_STATEMENT = "RETURN_STATEMENT"


# Define an AST Node to represent elements in the grammar
class ASTNode:
    def __init__(self, value: str, children: List[Any] = None):
        # TODO Validate correct value
        self.value = value
        self.children = children if children is not None else []

    def __repr__(self):
        return f"ASTNode(value={self.value}, children={self.children})"


# Define specific error handling
class ParserError(Exception):
    def __init__(self, message: str, token: Token = None):
        error_message = f"Parser error: {message}"
        if token:
            error_message += f" at token {token}"
        super().__init__(error_message)

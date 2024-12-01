from typing import List, Union, Any, Tuple
from lexer.models import Token, TokenType
from language.variables import Variables
from parser.models import ASTNode, ParserError


class EvaluationError(Exception):
    """Custom exception for errors during expression evaluation."""

    def __init__(self, message: str):
        super().__init__(f"Evaluation error: {message}")


class SyntaxParser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens

    def parse(self) -> ASTNode:
        """Parses a list of tokens into an AST."""

        # def parse_expression(index: int) -> tuple[ASTNode, int]:
        #     # Simple evaluation assuming tokens are in correct sequence of numbers and operators
        #     operand_stack: List[Union[int, float]] = []
        #
        #     for token in self.tokens:
        #         if token.type == "NUMBER":
        #             operand_stack.append(float(token.value))
        #         elif token.type in ("PLUS", "MINUS", "MULTIPLY", "DIVIDE"):
        #             if len(operand_stack) < 2:
        #                 raise EvaluationError("Insufficient operands for operation")
        #             b = operand_stack.pop()
        #             a = operand_stack.pop()
        #
        #             if token.type == "PLUS":
        #                 result = a + b
        #             elif token.type == "MINUS":
        #                 result = a - b
        #             elif token.type == "MULTIPLY":
        #                 result = a * b
        #             elif token.type == "DIVIDE":
        #                 if b == 0:
        #                     raise EvaluationError("Division by zero")
        #                 result = a / b
        #             operand_stack.append(result)
        #         else:
        #             raise EvaluationError(f"Unknown token {token.type}")
        #
        #     if len(operand_stack) != 1:
        #         raise EvaluationError("Invalid expression evaluation")
        #
        #     return operand_stack.pop()

        def parse_expression(index: int) -> tuple[ASTNode, int]:
            """Parse an expression with precedence handling."""
            left_node, index = parse_primary(index)
            while index < len(self.tokens) and self.tokens[index].type is TokenType.OPERATOR:
                operator_token = self.tokens[index]
                right_node, index = parse_primary(index + 1)
                left_node = ASTNode(value=operator_token.value, children=[left_node, right_node])
            return left_node, index

        def parse_primary(index: int) -> tuple[ASTNode, int]:
            """Parse primary expressions like variables or numbers."""
            token = self.tokens[index]
            if token.type in (TokenType.IDENTIFIER, TokenType.LITERAL):
                return ASTNode(value=f"{token.type}({token.value})"), index + 1
            raise ParserError("Unexpected token", token)

        def parse_if_statement(index: int) -> tuple[ASTNode, Any]:
            """Parse an if statement."""
            index += 1  # Skip IF

            assert self.tokens[index].type == TokenType.SEPARATOR and self.tokens[index].value == "(" # Opening Parenthesis
            index += 1

            condition, index = parse_expression(index) # Parse Expression

            assert self.tokens[index].type == TokenType.SEPARATOR and self.tokens[index].value == ")"  # Opening Parenthesis
            index += 1

            # Parse 'THEN' keyword
            if self.tokens[index].type != TokenType.KEYWORD or self.tokens[index].value != "then":
                raise ParserError("Expected THEN", self.tokens[index])
            index += 1

            assert self.tokens[index].type == TokenType.SEPARATOR and self.tokens[index].value == "{"  # Opening Parenthesis
            index += 1

            then_branch, index = parse_statement(index)

            assert self.tokens[index].type == TokenType.SEPARATOR and self.tokens[index].value == "}"  # Opening Parenthesis
            index += 1

            # Check for 'ELSE' clause
            if self.tokens[index].type != TokenType.KEYWORD or self.tokens[index].value != "else":
                raise ParserError("Expected ELSE", self.tokens[index])
            index += 1

            assert self.tokens[index].type == TokenType.SEPARATOR and self.tokens[index].value == "{"  # Opening Parenthesis
            index += 1

            else_branch, index = parse_statement(index)

            assert self.tokens[index].type == TokenType.SEPARATOR and self.tokens[index].value == "}"  # Opening Parenthesis
            index += 1

            return ASTNode(value='If', children=[condition, then_branch, else_branch]), index

        def parse_statement(index: int) -> tuple[ASTNode, Any] | ASTNode | int:
            """Parse a single statement."""
            token = self.tokens[index]
            if token.type == TokenType.KEYWORD and token.value == "print":
                expr_node, next_index = parse_expression(index + 1)
                return ASTNode(value='Print', children=[expr_node]), next_index
            elif token.type == TokenType.KEYWORD and token.value == "if":
                return parse_if_statement(index)
            else:
                raise ParserError("Invalid statement", token)

        def parse_program(index: int) -> tuple[ASTNode, int | Any]:
            """Parse a list of statements to form a complete program."""
            children = []
            while index < len(self.tokens):
                stmt_node, index = parse_statement(index)
                children.append(stmt_node)
            return ASTNode(value='Program', children=children), index

        try:
            ast, _ = parse_program(0)
            return ast
        except IndexError:
            raise ParserError("Incomplete expression")

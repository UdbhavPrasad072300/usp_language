import enum
from typing import List

from .models import Token, TokenType, Separator, Whitespace, Comment, Operators, Keywords, String


def is_character_in_enum(char: str, charactor_set: enum) -> bool:
    return any(char == item.value for item in charactor_set)


def lexer(file: str) -> List[Token]:
    tokens = []
    i = 0
    while i < len(file):
        character = file[i]

        # Separator
        if is_character_in_enum(character, Separator):
            token = Token(type=TokenType.SEPARATOR, value=character)
            tokens.append(token)
            i += 1

        # Identifiers/Keywords
        elif character.isalpha():
            start_index = i
            while i < len(file) and (file[i].isalpha() or file[i].isdigit()):
                i += 1
            identifier = file[start_index:i]

            if is_character_in_enum(identifier, Keywords):
                token = Token(type=TokenType.KEYWORD, value=identifier)
                tokens.append(token)
            else:
                token = Token(type=TokenType.IDENTIFIER, value=identifier)
                tokens.append(token)

        # Operators
        elif is_character_in_enum(character, Operators):
            token = Token(type=TokenType.OPERATOR, value=character)
            tokens.append(token)
            i += 1

        # Literal (numbers)
        elif character.isdigit():
            start_index = i
            used_dot = False
            while i < len(file) and (file[i].isdigit() or file[i] == "."):
                if file[i] == ".":
                    if used_dot:
                        raise Exception("Invalid literal")
                    used_dot = True
                i += 1
            literal = file[start_index:i]
            token = Token(type=TokenType.LITERAL, value=literal)
            tokens.append(token)

        # Literal (strings)
        elif character in ['\'', '\"']:
            start_index = i
            i += 1
            while i < len(file) and file[i] != character:
                i += 1
            i += 1
            literal = file[start_index:i]
            token = Token(type=TokenType.LITERAL, value=literal)
            tokens.append(token)

        # Whitespace
        elif is_character_in_enum(character, Whitespace):
            i += 1  # skip whitespace

        # Comments
        elif is_character_in_enum(character, Comment):
            while i < len(file) and file[i] != "\n":
                i += 1

        # Unknown Character
        else:
            raise Exception(f"Unexpected character: {character}")
            i += 1

    return tokens

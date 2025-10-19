from enum import Enum


class TokenType(Enum):
    """
    Enumeration for tokens type
    """
    T_KLEENE_CLOSURE = '*'
    T_LITERAL = 'literal'

class Token:
    """
    Token class define the structure of tokens
    """
    def __init__(self, type: TokenType, value: str) -> None:
        """
        Initialize token

        :param type: Type of token
        :param value: Value of token
        """
        self.type = type
        self.value = value

    def __repr__(self) -> str:
        """
        Helps in debugging

        :return: Formated String
        """
        return f"Token({self.type}, {self.value})"

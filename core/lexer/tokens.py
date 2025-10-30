from enum import Enum


class TokenType(Enum):
    """
    Enumeration for tokens type
    """
    # Rational Operations
    # Unary OP
    T_KLEENE_CLOSURE = '*' # Zero or plus of previous character
    # Binary OP
    T_PIPE = '|' # OR Op - One of the two operand

    T_LITERAL = 'literal'
    T_EPSILON = ''


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

from core.lexer.tokens import *


class Lexer:
    """
    Lexer class encapsulate all necessary functionality that help in Lexical Analysis
    """
    @staticmethod
    def tokenize(regex: str) -> list:
        """
        Helps to tokenize streams of lexemes to tokens
        (i.e. it helps distinguish between normal literal and reserved literal like *, +, |, (, ) and more ...)

        :param regex: Pattern
        :return: List of tokens (type, value)
        """
        tokens = []
        for c in regex:
            if c == '*':
                tokens.append(Token(TokenType.T_KLEENE_CLOSURE, '*'))
            elif c == '|':
                tokens.append(Token(TokenType.T_PIPE, '|'))
            elif c == '(':
                tokens.append(Token(TokenType.T_LEFT_PARENTHESES, '('))
            elif c == ')':
                tokens.append(Token(TokenType.T_RIGHT_PARENTHESES, ')'))
            else:
                tokens.append(Token(TokenType.T_LITERAL, c))

        return tokens

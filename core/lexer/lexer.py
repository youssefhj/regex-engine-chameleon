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
        :return List of tokens (type, value)
        """
        tokens = []
        tokens_can_be_escaped = ['*', '|', '`', '(', ')']
        i = 0
        while i < len(regex):
            if regex[i] == '*':
                tokens.append(Token(TokenType.T_KLEENE_CLOSURE, '*'))
            elif regex[i] == '|':
                tokens.append(Token(TokenType.T_PIPE, '|'))
            elif regex[i] == '(':
                tokens.append(Token(TokenType.T_LEFT_PARENTHESES, '('))
            elif regex[i] == ')':
                tokens.append(Token(TokenType.T_RIGHT_PARENTHESES, ')'))
            elif regex[i] == '`':
                i += 1

                if i >= len(regex):
                    raise SyntaxError("Unexpected escape character '`' at the end")

                if regex[i] not in tokens_can_be_escaped:
                    raise SyntaxError(f"Unexpected `{regex[i]}")

                tokens.append(Token(TokenType.T_LITERAL, regex[i]))
            else:
                tokens.append(Token(TokenType.T_LITERAL, regex[i]))

            i += 1

        return tokens
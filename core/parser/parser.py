from core.lexer.tokens import TokenType
from core.parser.tree.concat_node import ConcatNode
from core.parser.tree.kleen_node import KleeneNode
from core.parser.tree.literal_node import LiteralNode


class Parser:
    """
    Parse class encapsulate all necessary functionality for Syntax Analysis
    """
    pos = 0
    ll = 0
    tokens = None
    ast_stack = []
    ast = None

    @staticmethod
    def parse(tokens: list):
        """

        :param tokens:
        :return:
        :raise: Exception in case parsing error
        """
        # Regular Expression Grammar
        # REGEX -> LITERAL CONCAT
        # CONCAT -> KLEENE REGEX | KLEENE |  epsilon
        # LITERAL -> [a-zA-Z]
        # KLEENE -> '*' | epsilon

        Parser.ll = len(tokens)
        Parser.tokens = tokens

        if Parser.__regex() == True:
            # Build the AST Tree
            i = 0
            while i + 1 < len(Parser.ast_stack):
                if i == 0:
                    Parser.ast = Parser.ast_stack[i]
                Parser.ast = ConcatNode(Parser.ast, Parser.ast_stack[i + 1])
                i += 1

            return Parser.ast
        else:
            raise Exception(f'Error in parsing')

    @staticmethod
    def __regex():
        """

        :return:
        """
        if Parser.ll == 0:
            return False

        if Parser.pos >= Parser.ll:
            return True

        if Parser.__literal():
            literal_val = Parser.tokens[Parser.pos].value
            Parser.ast_stack.append(LiteralNode(literal_val))
            Parser.pos += 1

            return Parser.__concat()

        return False

    @staticmethod
    def __concat():
        if Parser.pos < Parser.ll:
            if Parser.__kleene():
                literal = Parser.ast_stack.pop()
                Parser.ast_stack.append(KleeneNode(literal))

                Parser.pos += 1

                if Parser.pos >= Parser.ll:
                    return True

            return Parser.__regex()

        return True


    @staticmethod
    def __literal():
        if Parser.tokens[Parser.pos].type is TokenType.T_LITERAL:
            return True

        return False

    @staticmethod
    def __kleene():
        if Parser.tokens[Parser.pos].type is TokenType.T_KLEENE_CLOSURE:
            return True

        return False

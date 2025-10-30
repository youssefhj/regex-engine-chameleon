from core.lexer.tokens import TokenType
from core.parser.tree.concat_node import ConcatNode
from core.parser.tree.kleen_node import KleeneNode
from core.parser.tree.literal_node import LiteralNode
from core.parser.tree.pipe_node import PipeNode


class Parser:
    """
    Parse class encapsulate all necessary functionality for Syntax Analysis
    """
    tokens = []
    pos, ll = 0, 0

    @staticmethod
    def parse(tokens: list):
        """
        Syntax Analyzer that parse incoming tokens, and generate AST

        :param tokens: List of tokens
        :return: Abstract Syntax Tree
        :raise: Exception in case parsing error
        """
        #== My REGEX Grammar
        # EXP     -> TERM SUBEXP
        # SUBEXP  -> `|` TERM SUBEXP | ε
        # TERM    -> FACTOR SUBTERM
        # SUBTERM -> * FACTOR SUBTERM | FACTOR SUBTERM | * | ε
        # FACTOR  -> literal
        Parser.ll = len(tokens)
        if Parser.ll <= 0: raise Exception('ERROR: Empty tokens list')

        Parser.tokens = tokens
        Parser.pos = 0

        return Parser.__exp()

    @staticmethod
    def __exp():
        """
        Handles the axiome rule

        :return: Abstract Syntax Tree
        """
        term = Parser.__term()

        ast = term

        sub_exp = Parser.__sub_exp()
        if sub_exp != '':
            ast = PipeNode(term, sub_exp)

        return ast

    @staticmethod
    def __sub_exp():
        """
        Handles expression with pipe `|` operator

        :return: PipeNode or ε
        """
        if Parser.__peek() is TokenType.T_PIPE:
            Parser.__eat()

            term = Parser.__term()
            sub_exp = Parser.__sub_exp()

            if sub_exp == '':
                return term

            return PipeNode(term, sub_exp)

        return ''

    @staticmethod
    def __term():
        """
        Handles the Kleene-closure `*` if exist

        :return: ConcatNode, KleeneNode, or LiteralNode
        :raise: Exception in case broken rule
        """
        if Parser.pos >= Parser.ll:
            raise Exception(f'ERROR_RULE_VIOLATED: we expect a literal at the end')

        factor = Parser.__factor()
        if factor is None:
            raise Exception(f'ERROR_RULE_VIOLATED: we expect a literal at position {Parser.pos + 1}')

        sub_term = Parser.__sub_term()

        if isinstance(sub_term, tuple):
            if sub_term[0] == '*':
                return ConcatNode(KleeneNode(factor), sub_term[1])
        elif sub_term == '':
            return factor
        elif sub_term == '*':
            return KleeneNode(factor)

        return ConcatNode(factor, sub_term)

    @staticmethod
    def __sub_term():
        """
        Handles the Kleene-closure with its sub terms if exist

        :return: ConcatNode, KleeneNode, LiteralNode, *,
                (*, ConcatNode), (*, KleeneNode), (*, LiteralNode), or ε
        :raise: Exception in case broken rule
        """
        if Parser.pos >= Parser.ll:
            return ''

        if Parser.__peek() is TokenType.T_KLEENE_CLOSURE:
            Parser.__eat()
            if Parser.pos >= Parser.ll:
                return '*'

            factor = Parser.__factor()
            if factor is None:
                return '*'

            sub_term = Parser.__sub_term()
            if isinstance(sub_term, tuple):
                if sub_term[0] == '*':
                    return '*', ConcatNode(KleeneNode(factor), sub_term[1])
            elif sub_term == '':
                return '*', factor
            elif sub_term == '*':
                return '*', KleeneNode(factor)

            return '*', ConcatNode(factor, sub_term)
        elif Parser.__peek() is TokenType.T_LITERAL:
            factor = Parser.__factor()
            if factor is None:
                raise Exception(f'ERROR_RULE_VIOLATED: we expect a literal at position {Parser.pos + 1}')

            sub_term = Parser.__sub_term()
            if isinstance(sub_term, tuple):
                if sub_term[0] == '*':
                    return ConcatNode(KleeneNode(factor), sub_term[1])
            elif sub_term == '':
                return factor
            elif sub_term == '*':
                return KleeneNode(factor)

            return ConcatNode(factor, sub_term)

        return ''

    @staticmethod
    def __factor():
        """
        Check if the current token is literal

        :return: LiteralNode if its valid
                 Otherwise None
        """
        token_val = Parser.tokens[Parser.pos].value

        if Parser.__peek() is TokenType.T_LITERAL:
            Parser.__eat()
            return LiteralNode(token_val)

        return None

    @staticmethod
    def __peek():
        """
        Make a look on the current token,
        and does not touch the cursor

        :return: The current token
        """
        if Parser.pos < Parser.ll:
            return Parser.tokens[Parser.pos].type

        return None

    @staticmethod
    def __eat():
        """
        Consume the current by incrementing the cursor

        :return: void
        """
        Parser.pos += 1
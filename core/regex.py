from copy import copy

from core.automaton import Automaton
from core.lexer.lexer import Lexer
from core.parser.parser import Parser
from core.parser.tree.kleen_node import KleeneNode
from core.parser.tree.literal_node import LiteralNode


class Regex:
    """
    Regex class encapsulate all methods that helps runs and evaluates regular expression
    """
    state = 0
    @staticmethod
    def match(literal: str, regex: str) -> bool:
        """
        Tells if the literal respect a certain pattern (i.e. regex)

        :param literal: A text
        :param regex: Regular Expression
        :return: True if the literal match the regex, False otherwise
        """

        automaton_DFA = Regex.__construct_automaton(regex) # Make a deterministic state machine
        state = next(iter(automaton_DFA.init_states)) # The entry to the state machine

        # We loop over each character in literal
        # if the character is not in the definition of alphabet of the d we simply return False
        # else we goto other state, and we keep doing that unit we reach the end of literal
        # Final step we check if the current state is the final state if so we return True otherwise False
        for c in literal:
            if c not in automaton_DFA.alphabet:
                return False

            if (state, c) not in automaton_DFA.transitions:
                return False

            state = Regex.__goto(automaton_DFA.transitions, state, c).pop()


        return state in automaton_DFA.final_states

    @staticmethod
    def __goto(transitions, state, symbol) -> set:
        """
        Goto from one state to another one based on symbol

        :param transitions: Set of transitions
        :param state: A state
        :param symbol: Symbol from alphabet
        :return:
        """
        return copy(transitions[(state, symbol)])

    @staticmethod
    def __construct_automaton(regex: str) -> Automaton:
        """
        Construct a deterministic d based on regex

        :param regex: Pattern
        :return: Automaton
        """
        # Lexing phase of the regex expression
        tokens = Lexer.tokenize(regex)

        # Parsing phase
        ast_tree = Parser.parse(tokens)

        Regex.state = 0

        # Construct Thompson d based on abstract syntax tree
        automaton = Regex.__construct_automaton_from_ast_nodes(ast_tree)

        return automaton.NFA_to_DFA()

    @staticmethod
    def __construct_automaton_from_ast_nodes(node) -> Automaton:
        """
        Construct d base on Abstract Syntax Tree

        :param node: Node of the tree
        :return: Epsilon-NFA
        """
        automaton = Automaton()
        if isinstance(node, LiteralNode):
            return Regex.__construct_automaton_from_literal_node(node, automaton)
        elif isinstance(node, KleeneNode):
            return Regex.__construct_automaton_from_kleene_node(node, automaton)
        else:
            return Regex.__construct_automaton_from_concat_node(node, automaton)

    @staticmethod
    def __construct_automaton_from_literal_node(node, automaton) -> Automaton:
        """
        Construct Automaton for literal node
        (i.e. literal(a) have equivalent d

            -->[0]--a-->[1]-->

            Automaton(alphabet = {a}, init_states = {0}, final_states = {1}, states = {0, 1}, transitions = {(0, a): 1})

        :param node: Literal node
        :param automaton: Automaton
        :return: Epsilon-NFA for node (e.g. a)
        """
        start = Regex.state
        Regex.state += 1
        end = Regex.state

        Regex.state += 1

        automaton.alphabet = {node.literal}
        automaton.init_states = {start}
        automaton.final_states = {end}
        automaton.states = {start, end}
        automaton.transitions = {
            (start, node.literal): {end}
        }

        return automaton

    @staticmethod
    def __construct_automaton_from_kleene_node(node, automaton) -> Automaton:
        """
        Construct Automaton for Kleene node
         (i.e. kleene(a) have equivalent d

                                 --epsilon--
                                v          |
            -->[0]--epsilon-->[1]---a--->[2]--epsilon-->[3]-->
                |                                        ^
               |_________________epsilon_________________|

            Automaton(alphabet = {a}, init_states = {0}, final_states = {3}, states = {0, 1, 2, 3},
                transitions = {(0, epsilon): 1, (1, a): 2, (2, epsilon): 1, (2, epsilon): 3, (0, epsilon): 3})

        :param node: Kleene node
        :param automaton: Automaton
        :return: Epsilon-NFA for Kleene (e.g. a*)
        """
        start = Regex.state

        Regex.state += 1
        first = Regex.state

        Regex.state += 1
        second = Regex.state

        Regex.state += 1
        end = Regex.state

        Regex.state += 1

        automaton.alphabet = {node.literal.literal}
        automaton.init_states = {start}
        automaton.final_states = {end}
        automaton.states = {start, first, second, end}
        automaton.transitions = {
            (start, ''): {first, end},
            (first, node.literal.literal):  {second},
            (second, ''): {first, end},
        }

        return automaton

    @staticmethod
    def __construct_automaton_from_concat_node(node, automaton) -> Automaton:
        """
        Construct Automaton for concatenation node
         (i.e. Concat(a, b) have equivalent d

            -->[0]--a-->[1]--epsilon-->[2]--b-->[3]-->

            Automaton(alphabet = {a, b}, init_states = {0}, final_states = {3}, states = {0, 1, 2, 3},
                transitions = {(0, a): 1 , (1, epsilon): 2, (2: b): 3})

        :param node: Concat node
        :param automaton: Automaton
        :return: Epsilon-NFA for concatenation (e.g. a.b)
        """
        thompson_automaton_left = Regex.__construct_automaton_from_ast_nodes(node.left)
        thompson_automaton_right = Regex.__construct_automaton_from_ast_nodes(node.right)

        # know we do Thompson d on concatenation `.`
        automaton.alphabet = thompson_automaton_left.alphabet.union(thompson_automaton_right.alphabet)
        automaton.init_states = thompson_automaton_left.init_states
        automaton.final_states = thompson_automaton_right.final_states
        automaton.states = thompson_automaton_left.states.union(thompson_automaton_right.states)

        automaton.transitions = {(thompson_automaton_left.final_states.pop(), ""): {thompson_automaton_right.init_states.pop()}}
        automaton.transitions.update(thompson_automaton_left.transitions)
        automaton.transitions.update(thompson_automaton_right.transitions)

        return automaton
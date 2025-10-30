from core.lexer.lexer import Lexer
from core.parser.parser import Parser
from core.regex import Regex

test_cases = ['a|b*c', 'b*c|a', 'a*', 'abcd', 'a|b', 'a*b*c*', 'a|b|c', 'a*|b|c', 'ad*|b*c']
for c in test_cases:
    print(f'\n------------- regex {c} -------------')
    tokens = Lexer.tokenize(c)
    print(tokens)
    print(Parser.parse(tokens))
    print('---------------------------------------')

print(Regex.match('if True else echo nice fi', 'if True else echo nice fi*'))
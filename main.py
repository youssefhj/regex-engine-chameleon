from core.lexer.lexer import Lexer
from core.parser.parser import Parser
from core.regex import Regex

test_cases = ['a|b*c', 'b*c|a', 'a*', 'abcd', 'a|b', 'a*b*c*', 'a|b|c', 'a*|b|c', 'ad*|b*c', 'a*(b|c)', '(a*b)|c', 'a*b|c', 'ab|c', 'a(b|c)', 'a(c)']
test_cases2 = ['aa*(b*)a|b']
for c in test_cases2:
    print(f'\n------------- regex {c} -------------')
    tokens = Lexer.tokenize(c)
    print(tokens)
    print(Parser.parse(tokens))
    print('---------------------------------------')

print(Regex.match('aa', 'aa*(b*)a|b'))
#print(Regex.match('abab', '(ab)*'))
#print(Regex.match('aab', '(a|b)*'))
#print(Regex.match('if False else echo nice fi', 'if (True|False) else echo nice fi*'))
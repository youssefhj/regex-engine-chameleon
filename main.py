from core.lexer.lexer import Lexer
from core.parser.parser import Parser
from core.regex import Regex

test_cases = ['a|b*c', 'b*c|a', 'a*', 'abcd', 'a|b', 'a*b*c*', 'a|b|c', 'a*|b|c', 'ad*|b*c', 'a*(b|c)', '(a*b)|c', 'a*b|c', 'ab|c', 'a(b|c)', 'a(c)', 'aa*(b*)a|b']

for c in test_cases:
    print(f'\n------------- regex {c} -------------')
    tokens = Lexer.tokenize(c)
    print(tokens)
    print(Parser.parse(tokens))
    print('---------------------------------------')

print(Regex.match('aabaa','ab*(b*)*a(b*(baa))'))

tokens = Lexer.tokenize('a*b|c')
print(tokens)

print(Parser.parse(tokens))

# Direct matching using the Regex module
truth = Regex.match('aaab', 'a*b|c')
print("Matching" if truth else "Unmatched")
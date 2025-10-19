from core.regex import Regex

print(Regex.match('if true then echo hello fi', 'if true then echo hello fi*'))
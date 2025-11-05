"""
Chameleon Regex Engine — CLI Mode
---------------------------------

This script allows you to quickly test regular expressions using
the Chameleon regex engine directly from the command line

Usage:
    python chameleon.py <pattern> <text>

Arguments:
    pattern : str
        The regular expression pattern you want to match
    text : str
        The string to test against the regex pattern
"""
import sys
from core.regex import Regex

# Validate command-line input
if len(sys.argv) < 3:
    print("Usage: python chameleon.py <pattern> <text>")
    sys.exit(1)

pattern = sys.argv[1] # First argument: regex pattern
text = sys.argv[2] # Second argument: string to match

# Run regex matching
truth = Regex.match(text, pattern)

# Display results
print("Chameleon Regex Engine — CLI Mode\n")
print(f"Pattern: {pattern}")
print(f"Text: {text}")
print("-" * 40)
print("Match!" if truth else "No match")
print("-" * 40)
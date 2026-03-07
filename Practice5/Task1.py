import re

pattern = r"ab*"

text = "abbb"
match = re.fullmatch(pattern, text)

if match:
    print("Match found")
else:
    print("No match")
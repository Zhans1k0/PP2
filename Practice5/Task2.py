import re

pattern = r"ab{2,3}"

text = "abbb"
match = re.fullmatch(pattern, text)

print("Match found" if match else "No match")
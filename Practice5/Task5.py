import re

pattern = r"a.*b"

text = "axxxb"
match = re.fullmatch(pattern, text)

print("Match found" if match else "No match")
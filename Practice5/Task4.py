import re

text = "London paris NewYork Tokyo"
pattern = r"[A-Z][a-z]+"

result = re.findall(pattern, text)
print(result)
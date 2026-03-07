import re

text = "HelloWorldPython"
result = re.sub(r"(?<!^)(?=[A-Z])", " ", text)

print(result)
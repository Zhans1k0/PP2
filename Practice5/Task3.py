import re

text = "hello_world test_case anotherExample"
pattern = r"[a-z]+_[a-z]+"

result = re.findall(pattern, text)
print(result)
import json

data = {
    "name": "Alice",
    "age": 21,
    "city": "Almaty"
}

json_string = json.dumps(data, indent=4)
print(json_string)

parsed = json.loads(json_string)
print(parsed["name"])

with open("data.json", "w") as file:
    json.dump(data, file, indent=4)

with open("data.json", "r") as file:
    loaded_data = json.load(file)

print(loaded_data)

loaded_data["grade"] = "A"
print(loaded_data)
import json

with open("D:/Download/dqs_address.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()

data = []

for line in lines:
    data.append(line)
print(len(data))
with open("D:/Download/dqs_address.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False)


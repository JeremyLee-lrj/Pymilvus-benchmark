import json
import random

data = []

num: int = 10000

for i in range(num):
    data.append([random.random() * 2 - 1 for _ in range(768)])

with open('generate_data.json', 'w') as file:
    json.dump(data, file)

print('Successfully generate data and serialize in generate_data.json')
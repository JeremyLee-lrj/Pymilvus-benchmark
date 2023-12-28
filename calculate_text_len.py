import json
import pickle

with open("./100w_0.pickle", "rb") as file:
    data: dict = pickle.load(file)

data_len: {int: int} = {}
num = len(data["text_list"])
for i in range(num):
    # print(len(data["text_list"][i]))
    cur_len = len(data["text_list"][i])
    if (cur_len in data_len.keys()):
        data_len[cur_len] += 1
    else:
        data_len[cur_len] = 1

data_len = dict(sorted(data_len.items(), key=lambda item: item[0]))
# print(data_len)
ma: int = 0
mi: int = int(2e9)
tot = 0
for key, value in data_len.items():
    ma = max(ma, key)
    mi = min(mi, key)
    tot += value

print(f"total number is {tot}")
print(f"max length is {ma}\nmin length is {mi}")
with open("data_len.json", "w") as file:
    json.dump(data_len, file)

print("Successfully calculate length of data")

import json

# open the json file containing the data
with open("../data_len.json", "r") as file:
    # load the data from the json file
    data: dict = json.load(file)

# initialize the total number of entries and the pointer
tot = 0
ptr = 0
# loop through the range of 10 to 231 by 10
for i in range(10, 231, 10):
    # loop through the entries in the data
    while (ptr < i):
        # check if the entry number is in the data
        if str(ptr) in data.keys():
            # add the number of entries to the total
            tot = tot + data[str(ptr)]
        # increment the pointer
        ptr += 1
    # print the number of entries which match the condition
    print("the number of entry which match the condition: "
          "entry_text_len < " + str(i) + " is " + str(tot))




# 这段注释是用CodeGeeX插件实现的，比较准确的注释了每一段代码。很强，很智能！
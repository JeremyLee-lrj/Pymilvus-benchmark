import pickle
import random

from pymilvus import (
    connections,
    Collection, FieldSchema, DataType, CollectionSchema,
)
import time

from pymilvus.orm import utility

# 连接 Milvus
conn = connections.connect(host="10.100.2.241", port=19530)

# 指定每个字段的 Schema
entry_id = FieldSchema("entry_id", DataType.INT64, is_primary=True)
entry_text = FieldSchema("entry_text", DataType.VARCHAR, max_length=1024)
entry_vector = FieldSchema("entry_vector", DataType.FLOAT_VECTOR, dim=768)
entry_text_len = FieldSchema("entry_text_len", DataType.INT64)
# 指定集合的 Schema
schema = CollectionSchema([entry_id, entry_text, entry_vector, entry_text_len])

# 创建空集合
utility.drop_collection("test_with_len")
collection = Collection("test_with_len", schema)
print("Successfully create collection")
# index_params = {
#     "metric_type": "L2",
#     "index_type": "IVF_FLAT",
#     "params": {"nlist": 1024},
# }
# collection.create_index("entry_vector", index_params)
# 读取 pickle 文件
pickle_file = "./100w_0.pickle"
with open(pickle_file, "rb") as f:
    data_dict: dict = pickle.load(f)

print("Successfully load data from 100w_0.pickle")

num = len(data_dict["text_list"])
data_id = [i for i in range(num)]
data_len = []
for i in range(num):
    data_len.append(len(data_dict["text_list"][i]))
tic = time.perf_counter()
i, step = 0, 2100
# num = 3000
while i < num:
    # 将数据插入集合
    collection.insert(
        [
            data_id[i: i + step],
            data_dict["text_list"][i: i + step],
            data_dict["text_vector"][i: i + step],
            data_len[i: i + step],  # 记录文本的长度，后续根据此进行hybrid search
        ]
    )
    i += step
    print(i)

# 确保所有数据被密封和索引
collection.flush()
toc = time.perf_counter()
print(f"inserted {num} entities in {toc - tic:0.4f} seconds")
#
start_time = time.perf_counter()
index_params = {
    "metric_type": "L2",
    "index_type": "IVF_FLAT",
    "params": {"nlist": 1024},
}
collection.create_index("entry_vector", index_params)
end_time = time.perf_counter()
print(f"Successfully created index in {end_time - start_time:0.4f} seconds")



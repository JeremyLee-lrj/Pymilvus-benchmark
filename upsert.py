from pymilvus import (
    connections,
    FieldSchema,
    DataType,
    CollectionSchema,
    utility,
    Collection,
)
import pickle
import time
import sys

# 连接 Milvus
conn = connections.connect(host="10.100.2.241", port=19530)

# 指定每个字段的 Schema
entry_id = FieldSchema("entry_id", DataType.INT64, is_primary=True)
entry_text = FieldSchema("entry_text", DataType.VARCHAR, max_length=1024)
entry_vector = FieldSchema("entry_vector", DataType.FLOAT_VECTOR, dim=768)

# 指定集合的 Schema
schema = CollectionSchema([entry_id, entry_text, entry_vector])

# 创建空集合
utility.drop_collection("test")
collection = Collection("test", schema)

pickle_file = "./100w_0.pickle"

with open(pickle_file, "rb") as f:
    # 读取 pickle 文件
    data_dict: dict = pickle.load(f)

num = len(data_dict["text_list"])
data_id = [i for i in range(num)]
tic = time.perf_counter()
i, step = 0, 2100
# print(type(data_dict))
while i < num / 2:
    # 将数据插入集合
    collection.insert(
        [
            data_id[i: i + step],
            data_dict["text_list"][i: i + step],
            data_dict["text_vector"][i: i + step],
        ]
    )
    i += step
    # print(i)
# 确保所有数据被密封和索引
collection.flush()
toc = time.perf_counter()
print(f"inserted {num / 2} entities in {toc - tic:0.4f} seconds")

start_time = time.perf_counter()
# 创建向量索引
index_params = {
    "metric_type": "L2",
    "index_type": "IVF_FLAT",
    "params": {"nlist": 1024},
}
collection.create_index("entry_vector", index_params)
end_time = time.perf_counter()
print(f"successfully create index in {end_time - start_time: 0.4f} seconds")

start_time = time.perf_counter()
while i < num:
    collection.upsert([
        data_id[i: i + step],
        data_dict["text_list"][i: i + step],
        data_dict["text_vector"][i: i + step]
    ])
    i += step
collection.flush()
end_time = time.perf_counter()

print(f"upserted {num - num / 2} entities in {end_time - start_time: 0.4f} seconds")

import json

from pymilvus import (
    connections,
    FieldSchema,
    DataType,
    CollectionSchema,
    utility,
    Collection, MilvusClient,
)

import time

# client = MilvusClient(
#     uri="http://10.100.2.241:19530"
# )
# 连接 Milvus
client = MilvusClient(
    uri="http://10.100.2.241:19530",
    token="root:Milvus",
    db_name="default"
)
# 指定每个字段的 Schema
entry_id = FieldSchema("entry_id", DataType.INT64, is_primary=True)
entry_text = FieldSchema("entry_text", DataType.VARCHAR, max_length=1024)
entry_vector = FieldSchema("entry_vector", DataType.FLOAT_VECTOR, dim=384)

# 指定集合的 Schema
schema = CollectionSchema([entry_id, entry_text, entry_vector])

# 创建空集合
utility.drop_collection("TextData")
collection = Collection("TextData", schema)


with open("/data/jeremy/dataset/TextSearch/dqs_address.json", "r", encoding="utf-8") as file:
    textData = json.load(file)

with open("/data/jeremy/dataset/TextSearch/dqs_address_embeddings.json", "r", encoding="utf-8") as file:
    textVec = json.load(file)

num = len(textData)
data_id = [i for i in range(num)]
tic = time.perf_counter()
i, step = 0, 2100

while i < num:
    # 将数据插入集合
    collection.insert(
        [
            data_id[i: i + step],
            textData[i: i + step],
            textVec[i: i + step],
        ]
    )
    i += step
    print(i)
# 确保所有数据被密封和索引
collection.flush()
toc = time.perf_counter()
print(f"inserted {num} entities in {toc - tic:0.4f} seconds")

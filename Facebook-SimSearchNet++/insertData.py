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
entry_id = FieldSchema(name="entry_id", dtype=DataType.INT64, is_primary=True)
entry_text = FieldSchema(name="entry_text", dtype=DataType.VARCHAR, max_length=1024)
entry_vector = FieldSchema(name="entry_vector", dtype=DataType.FLOAT_VECTOR, dim=384)

# 指定集合的 Schema
schema = CollectionSchema(fields=[entry_id, entry_text, entry_vector])

# 创建空集合
client.drop_collection(collection_name="TextData")
client.create_collection(collection_name="TextData", schema=schema)

with open("/home/bangsun-f/Jeremy/dataset/TextSearch/dqs_address.json", "r", encoding="utf-8") as file:
    textData = json.load(file)

with open("/home/bangsun-f/Jeremy/dataset/TextSearch/dqs_address_embeddings.json", "r", encoding="utf-8") as file:
    textVec = json.load(file)

num = len(textData)
data_id = [i for i in range(num)]
tic = time.perf_counter()
i, step = 0, 2100

while i < num:
    # 将数据插入集合
    cur_data = []
    ptr = i
    while (ptr < num) and ptr < i + step:
        cur_data.append({"entry_id": data_id[ptr], "entry_text": textData[ptr], "entry_vector": textVec[ptr]})
        ptr += 1
    client.insert(
        collection_name="TextData",
        data=cur_data
    )
    i += step
    print(i)
toc = time.perf_counter()
print(f"inserted {num} entities in {toc - tic:0.4f} seconds")

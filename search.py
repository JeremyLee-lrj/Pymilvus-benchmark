import json

from pymilvus import (
    connections,
    Collection,
)
import time
import random

# 连接 Milvus
conn = connections.connect(host="10.100.2.241", port=19530)

# 获取现有集合
collection = Collection("test_with_len")

# 搜索前必须先把集合加载进内存
collection.load()

with open('generate_data.json', 'r') as file:
    data = json.load(file)

count = 100000
tic = time.perf_counter()
for i in range(count):
    # 向量相似性搜索
    search_params = {"metric_type": "L2", "offset": 0, "params": {"nprobe": 10}}
    result = collection.search(
        data=[data[i]],
        anns_field="entry_vector",
        param=search_params,
        limit=1,
        output_fields=["entry_text"],
    )
toc = time.perf_counter()
print(f"searched {count} times in {toc - tic:0.4f} seconds")

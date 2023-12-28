import json
import pickle
from pymilvus import (
    connections,
    Collection, FieldSchema, DataType, CollectionSchema,
)
import time
import random
from pymilvus.orm import utility

# 连接 Milvus
conn = connections.connect(host="localhost", port=19530)

collection = Collection("test_with_len")
collection.load()

# start_time = time.perf_counter()
# index_params = {
#     "metric_type": "L2",
#     "index_type": "IVF_FLAT",
#     "params": {"nlist": 1024},
# }
# collection.create_index("entry_vector", index_params)
# end_time = time.perf_counter()
# print(f"Successfully created index in {end_time - start_time:0.4f} seconds")

# 将预先构造好的1w条数据导入
with open("generate_data.json", "rb") as file:
    data = json.load(file)

time_cost = {}
for i in range(10, 231, 10):
    tic = time.perf_counter()
    # 向量相似性搜索
    search_params = {
        "metric_type": "L2",
        "offset": 0,
        "params": {"nprobe": 10},
    }
    for j in range(0, 10000):
        result = collection.search(
            [data[j]],
            "entry_vector",
            search_params,
            limit=1,
            # expr="len(entry_text) < 2000000",
            output_fields=["entry_text", "entry_text_len", "entry_vector"],
            expr="entry_text_len < " + str(i),
        )
    toc = time.perf_counter()
    print(f"When entry_text_len < {i}, 10000 hybirdsearches finished in {toc - tic:0.4f} seconds")
    time_cost[i] = toc - tic

with open("res/hybridsearch_ls_res.json", "w") as file:
    json.dump(time_cost, file)

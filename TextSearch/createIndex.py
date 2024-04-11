import time

from pymilvus import connections, Collection, MilvusClient

client = MilvusClient(
    uri="http://10.100.2.241:19530",
    token="root:Milvus",
    db_name="default"
)
collection = Collection("TextData")

tic = time.perf_counter()
# 创建向量索引
index_params = {
    "metric_type": "L2",
    "index_type": "IVF_FLAT",
    "params": {"nlist": 1024},
}
collection.create_index("entry_vector", index_params)
toc = time.perf_counter()
# collection.drop_index()
print(f"Index building time: {toc - tic:0.4f} seconds")

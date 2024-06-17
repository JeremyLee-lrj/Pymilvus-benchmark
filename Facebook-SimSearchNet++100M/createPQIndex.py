import time

from pymilvus import connections, Collection, MilvusClient

client = MilvusClient(
    uri="http://10.100.2.241:19530",
    token="root:Milvus",
    db_name="default"
)

tic = time.perf_counter()
# 创建向量索引
index_params = MilvusClient.prepare_index_params()
index_params.add_index(
    field_name="entry_vector",
    metric_type="L2",
    index_type="IVF_PQ",
    params={"nlist": 1024, "m": 16},
    index_name="IVFPQ_index",
)
client.create_index(
    collection_name="Facebook_SimSearchNet100M",
    index_params=index_params
)
toc = time.perf_counter()
print(f"Index building time: {toc - tic:0.4f} seconds")

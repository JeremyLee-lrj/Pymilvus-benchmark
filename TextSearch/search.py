import json
import time

from pymilvus import connections, Collection, MilvusClient

client = MilvusClient(
    uri="http://10.100.2.241:19530",
    token="root:Milvus",
    db_name="default"
)

collection = Collection("TextData")

collection.load()
# load text and embeddings
with open("/data/jeremy/dataset/TextSearch/dqs_address.json", "r", encoding="utf-8") as file:
    textData = json.load(file)

with open("/data/jeremy/dataset/TextSearch/dqs_address_embeddings.json", "r", encoding="utf-8") as file:
    textVec = json.load(file)
# # 连接 Milvus
# conn = connections.connect(host="10.100.2.241", port=19530)
#
# # 获取现有集合
# collection = Collection("test_with_len")
#
# # 搜索前必须先把集合加载进内存
# collection.load()
#
# with open('generate_data.json', 'r') as file:
#     data = json.load(file)
#
# count = 100000
# tic = time.perf_counter()
# for i in range(count):
#     # 向量相似性搜索
#     search_params = {"metric_type": "L2", "offset": 0, "params": {"nprobe": 10}}
#     result = collection.search(
#         data=[data[i]],
#         anns_field="entry_vector",
#         param=search_params,
#         limit=1,
#         output_fields=["entry_text"],
#     )
# toc = time.perf_counter()
# print(f"searched {count} times in {toc - tic:0.4f} seconds")
num = 10
tic = time.perf_counter()

for i in range(num):
    print("Query textData is ", textData[i])

    search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
    res = collection.search(
        data=[textVec[i]],
        anns_field="entry_vector",
        param=search_params,
        limit=5,  # Max. number of search results to return
        output_fields=["entry_id", "entry_text"],
    )

    result = json.dumps(res, indent=4)
    with open("output.json", "a", encoding="utf-8") as file:
        file.write("Query data is " + textData[i] + "\n")
        file.write(result)

toc = time.perf_counter()
print(f"tic: {tic: 0.4f}")
print(f"toc: {toc: 0.4f}")
print(f"Time taken: {toc - tic: 0.4f} seconds")

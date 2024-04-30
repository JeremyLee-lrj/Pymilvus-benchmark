import json
import random
import time

from pymilvus import MilvusClient, Collection
from pymilvus import connections

connections.connect(
    uri="http://10.100.2.241:19530",
    token="root:Milvus"
)

client = MilvusClient(
    uri="http://10.100.2.241:19530",
    token="root:Milvus",
    db_name="default"
)
collection = Collection("Facebook_SimSearchNet100M")
# collection.release()
collection.set_properties({'mmap.enabled': True})

collection.alter_index(
    index_name="ivf_flat_index",
    extra_params={"mmap.enabled": True}
)
print("load start")
client.load_collection(collection_name="Facebook_SimSearchNet100M", timeout=1000000)
print("load finish")
num = 10
data = []
for i in range(num):
    data.append([random.random() * 2 - 1 for _ in range(256)])

tic = time.perf_counter()

for i in range(num):
    print("Query textData is ", data[i])

    res = client.search(
        collection_name="Facebook_SimSearchNet100M",
        data=[data[i]],
        anns_field="entry_vector",
        limit=5,  # Max. number of search results to return
        search_params={"metric_type": "L2", "params": {"nprobe": 10}},  # Search parameters
        output_fields=["entry_id", "entry_vector"],
    )

    result = json.dumps(res, indent=4)
    with open("output.json", "a", encoding="utf-8") as file:
        file.write("Query data is " + str(data[i]) + "\n")
        file.write(result)

toc = time.perf_counter()
print(f"tic: {tic: 0.4f}")
print(f"toc: {toc: 0.4f}")
print(f"Time taken: {toc - tic: 0.4f} seconds")

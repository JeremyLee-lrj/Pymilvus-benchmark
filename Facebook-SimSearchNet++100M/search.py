import json
import time

from pymilvus import MilvusClient, connections, Collection

client = MilvusClient(
    uri="http://10.100.2.241:19530",
    token="root:Milvus",
    db_name="default"
)

# load text and embeddings
with open("/home/bangsun-f/Jeremy/dataset/TextSearch/dqs_address.json", "r", encoding="utf-8") as file:
    textData = json.load(file)

with open("/home/bangsun-f/Jeremy/dataset/TextSearch/dqs_address_embeddings.json", "r", encoding="utf-8") as file:
    textVec = json.load(file)
client.load_collection(collection_name="TextData")
num = 10
tic = time.perf_counter()

for i in range(num):
    print("Query textData is ", textData[i])

    res = client.search(
        collection_name="TextData",  # Replace with the actual name of your collection
        # Replace with your query entry_idctorentry_text
        data=[textVec[i]],
        anns_field="entry_vector",
        limit=5,  # Max. number of search results to return
        search_params={"metric_type": "L2", "params": {"nprobe": 10}},  # Search parameters
        output_fields=["entry_id", "entry_text"],
    )

    result = json.dumps(res, indent=4)
    with open("output.json", "a", encoding="utf-8") as file:
        file.write("Query data is " + result + "\n")
        file.write(result)

toc = time.perf_counter()
print(f"tic: {tic: 0.4f}")
print(f"toc: {toc: 0.4f}")
print(f"Time taken: {toc - tic: 0.4f} seconds")

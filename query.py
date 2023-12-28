import json
from pymilvus import (
    connections,
    Collection,
)
import time

# 连接 Milvus
conn = connections.connect(host="10.100.2.241", port=19530)
# 获取现有集合
collection = Collection("test_with_len")
# 搜索前必须先把集合加载进内存
collection.load()

res = {}
# 设置步长为10，从10到230分别测试不同阈值
for i in range(10, 231, 10):
    expr = "entry_text_len < " + str(i)
    print("When " + expr, end=', ')
    tic = time.perf_counter()
    result = collection.query(
        expr=expr,
        output_fields=["entry_text", "entry_text_len"],
    )
    print(type(result))
    print(f"the number of result is {len(result)}", end=', ')
    toc = time.perf_counter()
    res[i] = toc - tic
    print(f"query finished in {toc - tic:0.4f} seconds")

with open("res/query_ls_res.json", "w") as file:
    json.dump(res, file)

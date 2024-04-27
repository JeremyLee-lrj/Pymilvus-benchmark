import json

import numpy as np
from pymilvus import (
    connections,
    FieldSchema,
    DataType,
    CollectionSchema,
    utility,
    Collection, MilvusClient,
)

import time

def read_fbin(filename, start_idx=0, chunk_size=None):
    """ Read *.fbin file that contains float32 vectors
    Args:
        :param filename (str): path to *.fbin file
        :param start_idx (int): start reading vectors from this index
        :param chunk_size (int): number of vectors to read.
                                 If None, read all vectors
    Returns:
        Array of float32 vectors (numpy.ndarray)
    """
    with open(filename, "rb") as f:
        nvecs, dim = np.fromfile(f, count=2, dtype=np.int32)
        # print(nvecs, dim)
        nvecs = (nvecs - start_idx) if chunk_size is None else chunk_size
        arr = np.fromfile(f, count=nvecs * dim, dtype=np.uint8,
                          offset=start_idx * 1 * dim)
    return arr.reshape(nvecs, dim)

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
entry_vector = FieldSchema(name="entry_vector", dtype=DataType.FLOAT_VECTOR, dim=256)

# 指定集合的 Schema
schema = CollectionSchema(fields=[entry_id, entry_vector])

# 创建空集合
client.drop_collection(collection_name="Facebook_SimSearchNet100M")
client.create_collection(collection_name="Facebook_SimSearchNet100M", schema=schema)

# data = read_fbin("FB_ssnpp_database.u8bin")

num = 100000000
# data_id = [i for i in range(num)]
tic = time.perf_counter()
i, step = 0, 2100

while i < num:
    # 将数据插入集合
    cnt = min(num - i, step)
    cur_data = read_fbin("/home/bangsun-f/Jeremy/dataset/Facebook-SimSearchNet++/FB_ssnpp_database.u8bin", i, cnt)
    ptr = i
    new_data = []
    for d in cur_data:
        data_list = []
        for dd in d:
            data_list.append(float(dd))
        new_data.append(data_list)
    cur_data = new_data
    insert_data = []
    while (ptr < num) and ptr < i + step:
        insert_data.append({"entry_id": ptr, "entry_vector": cur_data[ptr - i]})
        ptr += 1
    client.insert(
        collection_name="Facebook_SimSearchNet100M",
        data=insert_data
    )
    i = ptr
    print(i)
toc = time.perf_counter()
print(f"inserted {num} entities in {toc - tic:0.4f} seconds")

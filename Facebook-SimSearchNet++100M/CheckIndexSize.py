from pymilvus import connections, utility

connections.connect(
    uri="http://10.100.2.241:19530",
    token="root:Milvus"
)

# 查看集合的索引大小
index_name = "ivf_flat_index"
# status, sizes = milvus.get_index_build_progress(collection_name, index_name)
# Get the building progress of a specific index
res = utility.index_building_progress(
    collection_name="Facebook_SimSearchNet100M",
    index_name="ivf_flat_index"
)

print(res)

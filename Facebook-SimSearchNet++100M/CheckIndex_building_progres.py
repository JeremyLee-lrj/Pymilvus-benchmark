from pymilvus import MilvusClient, connections
from pymilvus.orm import utility

connections.connect(
    uri="http://10.100.2.241:19530",
    token="root:Milvus"
)
client = MilvusClient(
    uri="http://10.100.2.241:19530",
    token="root:Milvus",
    db_name="default"
)
res = utility.index_building_progress("Facebook_SimSearchNet100M", "IVFPQ_index")

print(res)

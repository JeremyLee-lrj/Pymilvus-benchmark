from pymilvus import FieldSchema, DataType, CollectionSchema

entry_id = FieldSchema("entry_id", DataType.INT64, is_primary=True)
entry_text = FieldSchema("entry_text", DataType.VARCHAR, max_length=1024)


schema = CollectionSchema([entry_id, entry_text])



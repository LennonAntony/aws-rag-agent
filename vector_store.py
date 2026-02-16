from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection

def connect():
    connections.connect(alias="default", host="localhost", port="19530")

def create_collection():
    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=1536),
        FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535)
    ]

    schema = CollectionSchema(fields)
    collection = Collection("knowledge_base", schema)

    collection.create_index(
        field_name="embedding",
        index_params={
            "metric_type": "COSINE",
            "index_type": "IVF_FLAT",
            "params": {"nlist": 128}
        }
    )

    return collection




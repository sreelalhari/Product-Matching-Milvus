import pandas as pd
df=pd.read_csv('all_data.csv')
#Vectorization of data
from sentence_transformers import SentenceTransformer
text = df["Title"].to_list()
encoder = SentenceTransformer("multi-qa-mpnet-base-dot-v1")
vectors = encoder.encode(text)
vectors.shape
# # Connect to Milvus
from pymilvus import connections
connections.connect(
  alias="default", 
  host='localhost', 
  port='19530'
)


# # Create Collection
from pymilvus import CollectionSchema, FieldSchema, DataType
product_id = FieldSchema(
  name="product_id", 
  dtype=DataType.INT64, 
  is_primary=True, 
)
embedding = FieldSchema(
  name="embedding", 
  dtype=DataType.FLOAT_VECTOR, 
  dim=768,
)
schema = CollectionSchema(
  fields=[product_id, embedding], 
  description="product_search"
)
collection_name = "product_collection"

from pymilvus import Collection
collection = Collection(
    name=collection_name, 
    schema=schema, 
    using='default', 
    shards_num=1
    )

product_vectors = vectors.tolist()
product_id = df['product_id'].values.tolist()
data=[product_id,product_vectors]

from pymilvus import Collection
collection = Collection("product_collection")      # Get an existing collection.
mr = collection.insert(data)

index_params = {
  "metric_type":"L2",
  "index_type":"IVF_FLAT",
  "params":{"nlist":1024}
}

from pymilvus import Collection
collection = Collection("product_collection")     
collection.create_index(
  field_name="embedding", 
  index_params=index_params
)


# #  Milvus Search

from pymilvus import Collection
collection = Collection("product_collection")      
collection.load()


search_params = {"metric_type": "L2", "params": {"nprobe": 10}, "offset": 5}


result_id_list=[]
result_distance_list=[]
for item in range(len(product_vectors)):
    results = collection.search(
        data=[product_vectors[item]], 
        anns_field="embedding", 
        param=search_params,
        limit=10, 
        expr=None,
        consistency_level="Strong"
    )
    result_id_list.append(results[0].ids[0])
    result_distance_list.append(results[0].distances[0])


product_id_list=list(range(1390))

result_df = pd.DataFrame(list(zip(product_id_list, result_id_list, result_distance_list)), columns=['product_id', 'similar_product_id', 'distance'])

result_df.head()

result_df.to_csv('result_data01.csv',index=False)




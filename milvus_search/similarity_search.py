# Import pandas library
import pandas as pd

# Read Amazon and Flipkart cleaned data from CSV files
amazon_df = pd.read_csv('amazon_cleaned_data.csv')
flipkart_df = pd.read_csv('flipkart_cleaned_data.csv')

# Remove rows with missing values
flipkart_df=flipkart_df.dropna()
amazon_df=amazon_df.dropna()

# Check for any missing values in Amazon data frame
amazon_df.isnull().sum()

# Concatenate Amazon and Flipkart data frames into a single data frame
df = pd.concat([amazon_df, flipkart_df])

# Import TfidfVectorizer from scikit-learn
from sklearn.feature_extraction.text import TfidfVectorizer

# Initialize TfidfVectorizer with English stop words and maximum of 128 features
vectorizer = TfidfVectorizer(stop_words='english', max_features=128)

# Fit and transform the concatenated data frame using TfidfVectorizer
vectors = vectorizer.fit_transform(df['Title']).toarray()

# Import connections module from pymilvus
from pymilvus import connections

# Connect to Milvus server
connections.connect(
  alias="default", 
  host='localhost', 
  port='19530'
)

# Import CollectionSchema, FieldSchema, and DataType from pymilvus
from pymilvus import CollectionSchema, FieldSchema, DataType

# Define product_id and embedding fields for the Milvus collection
product_id = FieldSchema(
  name="product_id", 
  dtype=DataType.INT64, 
  is_primary=True, 
)
embedding = FieldSchema(
  name="embedding", 
  dtype=DataType.FLOAT_VECTOR, 
  dim=128,
)

# Define the schema for the Milvus collection
schema = CollectionSchema(
  fields=[product_id, embedding], 
  description="product_search"
)

# Specify the name of the Milvus collection
collection_name = "product_details2"

# Import Collection module from pymilvus
from pymilvus import Collection

# Create a new Milvus collection with the specified name, schema, and number of shards
collection = Collection(
    name=collection_name, 
    schema=schema, 
    using='default', 
    shards_num=2
    )
    
# Import numpy library
import numpy as np

# Convert the TfidfVectorizer output to list
vectors1 = vectors.tolist()

# Get product IDs from the concatenated data frame and convert them to list
product_id = df['product_id'].values.tolist()

# Combine product IDs and TfidfVectorizer output into a list
data=[product_id,vectors1]

# Import Collection module from pymilvus
from pymilvus import Collection

# Get an existing Milvus collection
collection = Collection("product_details2")      

# Insert the data into the Milvus collection
mr = collection.insert(data)

# Specify index parameters
index_params = {
  "metric_type":"L2",
  "index_type":"IVF_FLAT",
  "params":{"nlist":1024}
}

# Import Collection module from pymilvus
from pymilvus import Collection

# Get an existing Milvus collection
collection = Collection("product_details2")   

# Create index on the embedding field of the Milvus collection
collection.create_index(
  field_name="embedding", 
  index_params=index_params
)

# Import Collection module from pymilvus
from pymilvus import Collection

# Get an existing Milvus collection
collection = Collection("product_details2")      

# Load the Milvus collection into memory
collection.load()

# Specify search parameters
search_params = {"metric_type": "L2", "params": {"nprobe": 10}, "offset": 5}

# Perform a vector similarity search on the collection
results = collection.search(
    data=[vectors1[15]],  # Query vector for which to find similar items
    anns_field="embedding",  # Name of the field containing the embeddings
    param=search_params,  # Search parameters, including the number of nearest neighbors to return
    limit=10,  # Maximum number of search results to return
    expr=None,  # Optional expression to filter the search results
    consistency_level="Strong"  # Consistency level to use for the search operation
)

# Retrieve the IDs of the search results with the lowest distances
result_ids = results[0].ids

# Retrieve the distances between the query vector and the search results
result_distances = results[0].distances

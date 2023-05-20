# import necessary libraries for vectoriation and milvus search

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from pymilvus import connections
from pymilvus import Collection
from pymilvus import CollectionSchema, FieldSchema, DataType

# Function to vectorize text columns using SentenceTransformer
# Inputs:
#   - df: DataFrame containing the data
#   - columns: List of columns to be vectorized
def vectorize_columns(df, columns):
    encoder = SentenceTransformer("multi-qa-mpnet-base-dot-v1")
    for column in columns:
        if column not in ['product_link', 'product_key', 'Actual_Price', 'Selling_Price']:
            text = df[column].fillna('').astype(str).to_list()
            vectors = encoder.encode(text)
            df[column] = pd.Series(vectors.tolist())
            
            
# Function to connect to Milvus server
# Inputs:
#   - alias: Alias for the connection
#   - host: Milvus server host address
#   - port: Milvus server port
def connect_to_milvus(alias, host, port):
    try:
        connections.connect(
            alias=alias,
            host=host,
            port=port
        )
        print(f"Connected to Milvus at {host}:{port} with alias '{alias}'")
    except Exception as e:
        print(f"Failed to connect to Milvus at {host}:{port} with alias '{alias}': {str(e)}")
                

# Function to create a collection in Milvus
# Inputs:
#   - collection_name: Name of the collection
#   - primary_key: Name of the primary key field
#   - vector_field: Name of the field containing the vectors
#   - desc: Description of the collection
def create_collection(collection_name, primary_key, vector_field, desc):
    field_schemas = [
        FieldSchema(
            name=primary_key,
            dtype=DataType.INT64,
            is_primary=True
        ),
        FieldSchema(
            name=vector_field,
            dtype=DataType.FLOAT_VECTOR,
            dim=768
        )
    ]

    schema = CollectionSchema(
        name=collection_name,
        fields=field_schemas,
        description=desc,
        primary_field=primary_key
    )

    collection = Collection(
        name=collection_name,
        schema=schema,
        using="default",
        shards_num=1
    )

    return collection
    
# Function to insert data into a collection in Milvus
# Inputs:
#   - df: DataFrame containing the data
#   - collection_name: Name of the target collection
#   - column_name: Name of the column containing the data to be inserted
def insert_data_to_collections(df, collection_name, column_name):
    product_key = df['product_key'].values.tolist()
    attribute_values = df[column_name].values.tolist()

    try:
        collection = Collection(collection_name)  # Get an existing collection
    except Exception as e:
        raise ValueError(f"Collection {collection_name} does not exist. Please create it before inserting data.") from e

    collection_data = [product_key, attribute_values]
    collection.insert(collection_data)
    
# Function to create an index on a field in a collection in Milvus
# Inputs:
#   - collection_name: Name of the target collection
#   - field_name: Name of the field on which the index will be created
#   - index_params: Parameters for the index creation    
def create_index(collection_name, field_name, index_params):
    try:
        collection = Collection(collection_name)  # Get an existing collection
    except Exception as e:
        raise ValueError(f"Collection {collection_name} does not exist. Please create it before creating an index.") from e

    collection.create_index(field_name=field_name, index_params=index_params)
    
# Function to perform similarity search in a collection in Milvus
# Inputs:
#   - collection_name: Name of the target collection
#   - search_params: Parameters for the search operation
#   - data: Data to search for similarities
#   - field_name: Name of the field containing vectors to search in
#   - limit: Maximum number of results to return
#   - search_query: Query expression for filtering the search results
#   - level: Consistency level for the search operation    
def similarity_search(collection_name,search_params,data,field_name,limit,search_query,level):    
    collection = Collection(collection_name)      
    collection.load()
  
    results = collection.search(
        data=data, 
        anns_field=field_name, 
        param=search_params,
        limit=limit, 
        expr=search_query,
        consistency_level=level
    )
    return results


# Function to filter search results based on a threshold
# Inputs:
#   - results: Search results
#   - threshold: Maximum distance threshold
def filter_results(results, threshold):
    filtered_results = {
        'ids': [],
        'distances': []
    }

    for i in range(len(results[0].distances)):
        if results[0].distances[i] <= threshold:
            filtered_results['ids'].append(results[0].ids[i])
            filtered_results['distances'].append(results[0].distances[i])

    return filtered_results
    
    
# Function to process the last result and generate final results
# Inputs:
#   - last_result: Last result to process
#   - source_df: DataFrame containing the source data
#   - target_df: DataFrame containing the target data
def process_results(last_result, source_df, target_df):
    final_result = {
        'Source_ID': [],
        'Similar_ID': [],
        'Source_Link': [],
        'Similar_Link': []
    }

    for item in range(len(last_result)):
        if last_result[item] == 'NaN':
            final_result['Source_ID'].append(item)
            final_result['Similar_ID'].append("NaN")
            final_result['Source_Link'].append(source_df['product_link'][item])
            final_result['Similar_Link'].append("NaN")
        else:
            filtered_results = filter_results(last_result[item], 30)
            if len(filtered_results['ids']) == 0:
                final_result['Source_ID'].append(item)
                final_result['Similar_ID'].append("NaN")
                final_result['Source_Link'].append(source_df['product_link'][item])
                final_result['Similar_Link'].append("NaN")
            else:
                final_result['Source_ID'].append(item)
                final_result['Similar_ID'].append(filtered_results['ids'][0])
                final_result['Source_Link'].append(source_df['product_link'][item])
                final_result['Similar_Link'].append(target_df['product_link'][filtered_results['ids'][0]])

    return final_result



# Performing the similarity search on Amazon dataset using flipkart data that we scraped before.

# Loading the datasets
amazon_df=pd.read_csv("amazon_final.csv")
flipkart_df=pd.read_csv("flipkart_final.csv")

# Vectorizing Both Dataframes

columns_to_vectorize = ['Title', 'Brand', 'Model', 'Colour', 'Form_Factor', 'Connectivity_Type']
# Calling the function on amazon data
vectorize_columns(amazon_df, columns_to_vectorize)
# Calling the function on flipkart data
vectorize_columns(flipkart_df, columns_to_vectorize)


# Colling the function to connect to the milvus server
connect_to_milvus("default", "localhost", "19530")

# Creating collections for the following vector fields using the function create_collection()
vector_fields = ["Title", "Brand", "Model","Colour", "Connectivity_Type","Form_Factor"]
for field in vector_fields:
    collection_name = f"{field}_collection"
    primary_key="product_key"
    desc=f"search_{field}"
    collection = create_collection(collection_name,primary_key,field,desc)
    
    
# Inserting data into the appropriate created collection using the function insert_data_to_collections()
for field in vector_fields:
    collection_name = f"{field}_collection"
    column_name=field
    df=amazon_df
    insert_data_to_collections(df, collection_name, column_name)

# Creating index for the vector field of all the collections using the below given index parameters and function defined before.

index_params = {
  "metric_type":"L2",
  "index_type":"IVF_FLAT",
  "params":{"nlist":1024}
}
create_index("Brand_collection", "Brand", index_params)
create_index("Model_collection", "Model", index_params)
create_index("Colour_collection", "Colour", index_params)
create_index("Connectivity_Type_collection", "Connectivity_Type", index_params)
create_index("Form_Factor_collection", "Form_Factor", index_params)
create_index("Title_collection", "Title", index_params)



# Conducting the similarity search on various levels based on the created collections usinng the similarity_search() function. Here each row of flipkart_df is searched on milvus on each iteration

# First We Search on Brand
result_list=[]
for item in range(0,flipkart_df.shape[0]):    
    collection_name = "Brand_collection"
    search_params = {"metric_type": "L2", "params": {"nprobe": 10}, "offset": 5}
    data = [np.array(flipkart_df['Brand'][item])]
    field_name = "Brand"
    limit = 1000
    search_query = None
    level = "Strong"
    result=similarity_search(collection_name,search_params,data,field_name,limit,search_query,level)
    result_list.append(result)
    
# Filtering the result from the search based on a threshold distance <=0 using filter_results() function
filtered_result_list=[]
for result in result_list:
    filtered_result= filter_results(result, 0)
    filtered_result_list.append(filtered_result)
    
# Now we conduct the search on the result of first search based on the Form_Factor column of the dataframe.
result_list_level2=[]
for item in range(0,flipkart_df.shape[0]):    
    collection_name = "Form_Factor_collection"
    search_params = {"metric_type": "L2", "params": {"nprobe": 10}, "offset": 5}
    data = [np.array(flipkart_df['Form_Factor'][item])]
    field_name = "Form_Factor"
    limit = 1000
    search_query = f"product_key in {filtered_result_list[item]['ids']}"
    level = "Strong"
    result=similarity_search(collection_name,search_params,data,field_name,limit,search_query,level)
    result_list_level2.append(result) 
    
#Filtering that result based on threshold distance <=0 using filter_results() function
filtered_result_list_level2=[]
for result in result_list_level2:
    filtered_result= filter_results(result, 0)
    filtered_result_list_level2.append(filtered_result)
    
# Repeating the search on colour column
result_list_level3=[]
for item in range(0,flipkart_df.shape[0]):    
    collection_name = "Colour_collection"
    search_params = {"metric_type": "L2", "params": {"nprobe": 10}, "offset": 5}
    data = [np.array(flipkart_df['Colour'][item])]
    field_name = "Colour"
    limit = 1000
    search_query = f"product_key in {filtered_result_list_level2[item]['ids']}"
    level = "Strong"
    result=similarity_search(collection_name,search_params,data,field_name,limit,search_query,level)
    result_list_level3.append(result) 

#Filtering
filtered_result_list_level3=[]
for result in result_list_level3:
    filtered_result= filter_results(result, 0)
    filtered_result_list_level3.append(filtered_result)
    
# Now finally conducting the search on Title Column
result_list_level4=[]
for item in range(0,flipkart_df.shape[0]):
    if len(filtered_result_list_level3[item]['ids'])==0:
        result_list_level4.append("NaN")
    else:
        collection_name = "Title_collection"
        search_params = {"metric_type": "L2", "params": {"nprobe": 10}, "offset": 5}
        data = [np.array(flipkart_df['Title'][item])]
        field_name = "Title"
        limit = 1000
        search_query = f"product_key in {filtered_result_list_level3[item]['ids']}"
        level = "Strong"
        result=similarity_search(collection_name,search_params,data,field_name,limit,search_query,level)
        result_list_level4.append(result) 
        
#Filtering
filtered_result_list_level4=[]
for result in result_list_level4:
    filtered_result= filter_results(result, )
    filtered_result_list_level3.append(filtered_result)
    
    
# Now Processing the latest found result to create the final result using the function process_result().

final_df=process_results(result_list_level4,flipkart_df,amazon_df)

# Saving as a csv file containing, Product details from flipkart under Source_ID and Source_Link columns and if similar product is available on the amazon database, that product is listed under Similar_ID, and Similar_Link column

final_df.to_csv('final_result.csv',index=False)

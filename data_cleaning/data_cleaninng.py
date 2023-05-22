# import necessary libraries
import pandas as pd

# Defining few functions to clean the dataset. Explanation about each function is provided above the function.

    """
    Load the CSV file into a DataFrame.
    Args: file_path (str): Path to the CSV file.
    Returns: pandas.DataFrame: Loaded DataFrame.
    """
def load_csv(file_path):
    return pd.read_csv(file_path)


    """
    Remove specified columns from the DataFrame.
    Args: dataframe (pandas.DataFrame): Input DataFrame.
          columns (list): List of column names to be removed.
    Returns: pandas.DataFrame: Loaded DataFrame.
    """
def remove_columns(dataframe, columns):
    return dataframe.drop(columns=columns)


    """
    Merge values from multiple columns into a single column.
    Args: row (pandas.Series): Input row of the DataFrame.
          cols (list): List of column names to be merged.
    Returns: str: Merged values from the specified columns.
    """
def merge_columns(row, cols):
    merged_values = [str(row[col]) for col in cols if str(row[col]) != 'nan']
    return ' '.join(merged_values) if merged_values else None


    """
    Clean and convert price values to float.
    Args: price (str): Input price value as a string.
    Returns: float: Cleaned price value.
    """
def clean_price(price):
    if pd.isnull(price):
        return None
    else:
        return float(price.replace('₹', '').replace(',', ''))
    
    
    """
    Rename a column in the DataFrame.
    Args: dataframe (pandas.DataFrame): Input DataFrame.
          old_name (str): Current name of the column.
          new_name (str): New name for the column.
    Returns: pandas.DataFrame: DataFrame with the column renamed.
    """
def rename_columns(dataframe, old_name, new_name):
    dataframe.rename(columns={old_name: new_name}, inplace=True)
    return dataframe


    """
    Categorize connectivity types as "Wired" or "Wireless".    
    Args: connectivity (str): Input connectivity value.    
    Returns: str: Categorized connectivity type.
    """
def categorize_connectivity(connectivity):
    wired_keywords = ['wired']
    wireless_keywords = ['wireless', 'bluetooth']
    
    for keyword in wired_keywords:
        if keyword in str(connectivity).lower():
            return 'Wired'
    
    for keyword in wireless_keywords:
        if keyword in str(connectivity).lower():
            return 'Wireless'
    
    return None


    """
    Create a new 'Brand' column based on the 'Title' column.
    """
def create_brand_column(dataframe):
    dataframe['Brand'] = dataframe['Title'].str.split().str[0]
    return dataframe


    """
    Reindex the columns in the DataFrame.
    """
def reindex_columns(dataframe, columns):
    return dataframe.reindex(columns=columns)


    """
    Replace values in the 'Form_Factor' column.
    """
def replace_form_factor(dataframe):
    dataframe["Form_Factor"] = dataframe["Form_Factor"].replace({"True Wireless": "In Ear", "In the Ear": "In Ear", "On the Ear": "On Ear"})
    return dataframe


    """
    Save the DataFrame to a CSV file.    
    Args: dataframe (pandas.DataFrame): DataFrame to be saved.
          file_path (str): Path to save the CSV file.
    """
def save_to_csv(dataframe, file_path):
    dataframe.to_csv(file_path, index=False)
    
    
    """
    Clean the input CSV file based on the specified operations and save the result to a new CSV file.    
    Args: input_file (str): Path to the input CSV file.
          output_file (str): Path to save the cleaned CSV file.
          operations (list): List of operations to be applied on the DataFrame.
    """
def clean_data(input_file, output_file, operations):
    # Load the CSV file
    df = load_csv(input_file)

    # Apply operations
    for operation in operations:
        if operation['type'] == 'drop':
            df = remove_columns(df, operation['columns'])
        elif operation['type'] == 'merge':
            df[operation['target']] = df.apply(lambda row: merge_columns(row, operation['columns']), axis=1)
            df.drop(columns=operation['columns'], inplace=True)
        elif operation['type'] == 'clean_price':
            df[operation['column']] = df[operation['column']].apply(clean_price)
        elif operation['type'] == 'rename':
            df = rename_columns(df, operation['old_name'], operation['new_name'])
        elif operation['type'] == 'categorize_connectivity':
            df[operation['column']] = df[operation['column']].apply(categorize_connectivity)
        elif operation['type'] == 'reindex':
            df = reindex_columns(df, operation['columns'])
        elif operation['type'] == 'create_brand_column':
            df = create_brand_column(df)
        elif operation['type'] == 'replace_form_factor':
            df = replace_form_factor(df)

    # Drop rows with any null values
    df.dropna(inplace=True)
    
    # Add a primary key column
    df.insert(0, 'product_key', range(len(df)))

    # Save the cleaned dataframe to CSV
    save_to_csv(df, output_file)

# Clean the input CSV file with specified operations and save the result to a new CSV file.

# Firstly we apply the function on amazon_product_details.csv
input_file_amazon = 'amazon_product_details.csv'
output_file_amazon = 'amazon_cleaned_data.csv'
operations_amazon = [
    {'type': 'drop', 'columns': ['Special Feature', 'Mounting Hardware', 'Series', 'Included Components', 'Material', 'Compatible Devices', 'Item Dimensions LxWxH']},
    {'type': 'merge', 'columns': ['Headphones form factor', 'Form Factor'], 'target': 'Form_Factor'},
    {'type': 'merge', 'columns': ['Connector Type', 'Connectivity technologies', 'Wireless Communication Technology', 'Connectivity Technology'], 'target': 'Connectivity_Type'},
    {'type': 'clean_price', 'column': 'Actual_Price'},
    {'type': 'clean_price', 'column': 'Selling_Price'},
    {'type': 'rename', 'old_name': 'Model Name', 'new_name': 'Model'},
    {'type': 'categorize_connectivity', 'column': 'Connectivity_Type'}
]

clean_data(input_file_amazon, output_file_amazon, operations_amazon)


#Now we can apply on flipkart_product_details.csv.
input_file_flipkart = 'flipkart_product_details.csv'
output_file_flipkart = 'flipkart_cleaned_data.csv'
operations_flipkart = [
    {'type': 'drop', 'columns': ['Headphone Design', 'Accessories Included', 'Inline Remote', 'Sales Package', 'Type']},
    {'type': 'rename', 'old_name': 'Model Name', 'new_name': 'Model'},
    {'type': 'rename', 'old_name': 'Color', 'new_name': 'Colour'},
    {'type': 'rename', 'old_name': 'Connectivity', 'new_name': 'Connectivity_Type'},
    {'type': 'rename', 'old_name': 'Headphone Type', 'new_name': 'Form_Factor'},
    {'type': 'clean_price', 'column': 'Actual_Price'},
    {'type': 'clean_price', 'column': 'Selling_Price'},
    {'type': 'reindex', 'columns': ['product_link', 'Title', 'Actual_Price', 'Selling_Price', 'Brand', 'Model', 'Colour', 'Form_Factor', 'Connectivity_Type']},
    {'type': 'create_brand_column'},
    {'type': 'replace_form_factor'},
    {'type': 'categorize_connectivity', 'column': 'Connectivity_Type'}
]

clean_data(input_file_flipkart, output_file_flipkart, operations_flipkart)

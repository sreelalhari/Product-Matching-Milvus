import pandas as pd
import string
import spacy
import re

# Load the spaCy English model
nlp = spacy.load("en_core_web_sm")

# Preprocessing function for text columns:
    """
    Preprocesses the given text by converting to lowercase, removing punctuation,
    performing tokenization and lemmatization using the spaCy model, and removing
    consecutive whitespace characters.
    """
def preprocess_text(text):

    # Convert to lowercase
    text = text.lower()

    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))

    # Tokenization and lemmatization
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc]

    # Join tokens back into a single string
    processed_text = ' '.join(tokens)

    # Remove consecutive whitespace, allowing only a single whitespace character
    processed_text = re.sub(r'\s{2,}', ' ', processed_text)

    return processed_text


# Load the dataframe from CSV file
def load_dataframe(file_path):
    return pd.read_csv(file_path)


# Preprocess text columns in the dataframe
    """
    Preprocesses the specified columns in the dataframe by applying the preprocess_text
    function to each value.
    """
def preprocess_dataframe(dataframe, columns_to_preprocess):

    for column in columns_to_preprocess:
        dataframe[column] = dataframe[column].apply(preprocess_text)
    return dataframe


# Save the dataframe to CSV file
def save_dataframe(dataframe, file_path):

    dataframe.to_csv(file_path, index=False)
    

# Preprocess the input file and save the result to the output file
    """
    Preprocesses the input file by loading the dataframe, applying the preprocessing to
    the specified columns, and saving the result to the output file.
    """
def preprocess_and_save(input_file, output_file, columns_to_preprocess):

    dataframe = load_dataframe(input_file)
    dataframe = preprocess_dataframe(dataframe, columns_to_preprocess)
    save_dataframe(dataframe, output_file)
    

# Specify input and output file paths
amazon_input_file = 'amazon_cleaned_data.csv'
amazon_output_file = 'amazon_final.csv'
flipkart_input_file = 'flipkart_cleaned_data.csv'
flipkart_output_file = 'flipkart_final.csv'

# Specify columns to preprocess
amazon_columns_to_preprocess = ['Title', 'Brand', 'Model', 'Colour', 'Form_Factor', 'Connectivity_Type']
flipkart_columns_to_preprocess = ['Title', 'Brand', 'Model', 'Colour', 'Form_Factor', 'Connectivity_Type']

# Preprocess and save the Amazon data
preprocess_and_save(amazon_input_file, amazon_output_file, amazon_columns_to_preprocess)

# Preprocess and save the Flipkart data
preprocess_and_save(flipkart_input_file, flipkart_output_file, flipkart_columns_to_preprocess)


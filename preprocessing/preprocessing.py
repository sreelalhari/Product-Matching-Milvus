import pandas as pd
import string
import spacy
import re

# Load the spaCy English model
nlp = spacy.load("en_core_web_sm")

# Preprocessing function for text columns
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

# Load the dataframe
amazon_df = pd.read_csv('amazon_cleaned_data.csv')
flipkart_df = pd.read_csv('flipkart_cleaned_data.csv')

# Apply preprocessing to the necessary columns

amazon_df['Title'] = amazon_df['Title'].apply(preprocess_text)
amazon_df['Brand'] = amazon_df['Brand'].apply(preprocess_text)
amazon_df['Model'] = amazon_df['Model'].apply(preprocess_text)
amazon_df['Colour'] = amazon_df['Colour'].apply(preprocess_text)
amazon_df['Form_Factor'] = amazon_df['Form_Factor'].apply(preprocess_text)
amazon_df['Connectivity_Type'] = amazon_df['Connectivity_Type'].apply(preprocess_text)

flipkart_df['Title'] = flipkart_df['Title'].apply(preprocess_text)
flipkart_df['Brand'] = flipkart_df['Brand'].apply(preprocess_text)
flipkart_df['Model'] = flipkart_df['Model'].apply(preprocess_text)
flipkart_df['Colour'] = flipkart_df['Colour'].apply(preprocess_text)
flipkart_df['Form_Factor'] = flipkart_df['Form_Factor'].apply(preprocess_text)
flipkart_df['Connectivity_Type'] = flipkart_df['Connectivity_Type'].apply(preprocess_text)

#adding a primary key column
amazon_df.insert(0, 'product_key', range(len(amazon_df)))
flipkart_df.insert(0, 'product_key', range(len(flipkart_df)))

#saving the files
amazon_df.to_csv('amazon_final.csv',index=False)
flipkart_df.to_csv('flipkart_final.csv',index=False)

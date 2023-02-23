import pandas as pd

# Read the CSV file
df = pd.read_csv('flipkart_product_details.csv')

# Remove columns with names starting with "Unnamed"
df.drop(df.columns[df.columns.str.startswith('Unnamed')], axis=1, inplace=True)

# Drop unwanted columns
df = df.drop(columns=['Headphone Design', 'Accessories Included', 'Inline Remote', 'Sales Package'])

# Replace values in "Headphone Type" column
df["Headphone_Type"] = df["Headphone Type"].replace({"True Wireless": "In Ear", "In the Ear": "In Ear", "On the Ear": "On Ear"})

# Drop the original "Headphone Type" column
df = df.drop(columns=["Headphone Type"])

#creating a brand column to match with amzon data.
df['Brand'] = df['Title'].str.split().str[0]
df=df.rename(columns={'Model Name':'Model','Color': 'Colour','Connectivity':'Connectivity_Type','Headphone_Type':'Form_Factor'})
df=df.reindex(columns=['Title', 'Actual_Price', 'Selling_Price', 'Brand', 'Model', 'Colour', 'Form_Factor', 'Connectivity_Type'])

#coverting prices columns into floats by removing rupee symbol

def clean_price(price):
    if pd.isnull(price):
        return None
    else:
        return float(price.replace('₹', '').replace(',', ''))

#apply the function
df['Actual_Price'] = df['Actual_Price'].apply(clean_price)
df['Selling_Price'] = df['Selling_Price'].apply(clean_price)

# Save the updated DataFrame to a new CSV file
df.to_csv('flipkart_cleaned_data.csv', index=False)

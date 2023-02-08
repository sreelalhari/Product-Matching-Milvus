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

# Save the updated DataFrame to a new CSV file
df.to_csv('flipkart_cleaned_data.csv', index=False)

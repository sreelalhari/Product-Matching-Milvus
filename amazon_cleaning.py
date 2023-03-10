import pandas as pd
# load the csv file
df = pd.read_csv('amazon_product_details.csv')



# remove the columns with 'Unnamed' in their name
df.drop(df.columns[df.columns.str.startswith('Unnamed')], axis=1, inplace=True)

# drop unnecessary columns
cols_to_drop = ['Cable Type', 'Compatible Device', 'Special Feature', 'Style', 'Age Range (Description)', 'Mounting Hardware', 'Series', 'Compatible Devices', 'Specific Uses For Product', 'Material', 'Fabric Type', 'Weight', 'Size', 'Item Dimensions LxWxH', 'Number of Batteries']
data = df.drop(columns=cols_to_drop)

# define a custom function to merge columns
def merge_columns(row, col1, col2):
    return str(row[col2]) if row[col1] == 'nan' else str(row[col1])

# merge the 'Headphones Form Factor' and 'Form Factor' columns into 'Form_Factor'
data['Form_Factor'] = data.apply(lambda row: merge_columns(row, 'Headphones Form Factor', 'Form Factor'), axis=1)
data = data.drop(columns=['Headphones Form Factor', 'Form Factor'])

# define a custom function to merge columns
def merge_connectivity_columns(row, col1, col2, col3, col4, col5, col6):
    for col in (col1, col2, col3, col4, col5, col6):
        if row[col] != 'nan':
            return str(row[col])

# merge columns 'Connector Type', 'Connectivity technologies', 'Wireless Communication Technology', 'Connectivity Technology', 'Wireless communication technologies', 'Connectivity Type' into 'Connectivity_Type'
data['Connectivity_Type'] = data.apply(lambda row: merge_connectivity_columns(row, 'Connector Type', 'Connectivity technologies', 'Wireless Communication Technology', 'Connectivity Technology', 'Wireless communication technologies', 'Connectivity Type'), axis=1)
data = data.drop(columns=['Connector Type', 'Connectivity technologies', 'Wireless Communication Technology', 'Connectivity Technology', 'Wireless communication technologies', 'Connectivity Type'])

#coverting prices columns into floats by removing rupee symbol
def clean_price(price):
    if pd.isnull(price):
        return None
    else:
        return float(price.replace('???', '').replace(',', ''))
    
#apply the function
data['Actual_Price'] = data['Actual_Price'].apply(clean_price)
data['Selling_Price'] = data['Selling_Price'].apply(clean_price)
data=data.rename(columns={'Model Name':'Model'})

# save the data to a new csv file
data.to_csv('amazon_cleaned_data.csv', index=False)

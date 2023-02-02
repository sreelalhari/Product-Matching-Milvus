import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# List of Brand names to search for
Brand_Name=['boAt',  'Boult Audio', 'Mivi', 'JBL', 'ZEBRONICS',  'SONY', 'Ubon',  'Jabra', 'GoSale', 'Shop Reals']

# List to store all links to product pages
Links=[]

# Initializing the webdriver
browser = webdriver.Chrome()

# Looping through the Brand names to search on Amazon
for p in range(len(Brand_Name)):
    # Constructing the URL with the brand name to search
    URL='https://www.amazon.in/s?k=headphones&i=electronics&bbn=1388921031&rh=n%3A1388921031%2Cp_89%3A{}&dc&page=1&crid=26YCJ7VB7YLJ4&qid=1675167468&rnid=3837712031&sprefix=%2Caps%2C1567&ref=sr_pg_'.format(Brand_Name[p])
    # Looping through 3 pages of results for each brand
    for k in range(1,4):
        # Replacing the page number in the URL
        url = URL.replace("page=1", "page={}".format(k))
        new_url=url+'{}'.format(k)
        # Loading the URL in the browser
        browser.get(new_url)
        # Finding the links to product pages
        elem=browser.find_elements(By.XPATH,"//a[@class='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal']")
        links = [i.get_attribute("href") for i in elem]
        # Adding the links to the list
        Links.append(links)
    # Waiting for 3 seconds between each brand search
    time.sleep(3)

# Lists to store product information
an=[]
bn=[]
cn=[]
dn=[]
en=[]
fn=[]
gn=[]
hn=[]

# Merging all sublists of links into a single list
merged_list = []
for sublist in Links:
    merged_list.extend(sublist)
# Removing duplicate links
merged_list=list(set(merged_list))

# Function to extract product specifications
def extract_specifications(rows):
    # Join the elements of the list into a single string
    for row in rows:
        try:
            # Finding the product specifications
            cols = row.find_elements(By.XPATH, '//span[@class="a-size-base po-break-word"]')
            cols = [col.text for col in cols]
        except:
            cols='N.A'
    return cols

# Looping through each product link

for i in range(len(merged_list)):

    browser.get(merged_list[i])
    elem1=browser.find_element(By.XPATH,'//span[@class="a-size-large product-title-word-break"]')
    text=elem1.text
    an.append(text)

    try:
        elem2=browser.find_element(By.XPATH,'//span[@class="a-price-whole"]')
        text2=elem2.text
    except:
        text2='N.A'
        pass
        
  
    bn.append(text2)
    try:
        elem3 = browser.find_element(By.XPATH,'//table[@class="a-normal a-spacing-micro"]')
        rows = elem3.find_elements(By.TAG_NAME, "tr")
        col=extract_specifications(rows)


        
    except:
        text3='N.A'
        pass
    
    cols=extract_specifications(rows)
    if len(cols)==5:
        cn.append(cols[0])
        dn.append(cols[1])
        en.append(cols[2])
        fn.append(cols[3])
        gn.append(cols[4])
    else:    
        cn.append('N.A')
        dn.append('N.A')
        en.append('N.A')
        fn.append('N.A')
        gn.append('N.A')



        
        

#Converting Lists to Data Frame
df=pd.DataFrame([an,bn,cn,dn,en,fn,gn])
df=df.transpose()
df.columns = ['Title', 'Price','Brand','Model Name','Colour','Form factor','Connector Type']


#Converting List to CSV
df.to_csv('Amazon_headphones.csv', index=False) 

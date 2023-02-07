# Importing required libraries from selenium 
from selenium import webdriver
from selenium.webdriver.common.by import By

# Importing exception handling libraries
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

def get_product_links(base_url, brand_list):
    # Initialize an empty list to store the links
    links = []
    
    # Loop through each brand in the list
    for brand in brand_list:
        # Format the base URL with the current brand
        url = base_url.format(brand)
        
        # Initialize the webdriver
        browser = webdriver.Chrome()
        
        # Navigate to the URL
        browser.get(url)
        
        # Counter to keep track of the number of pages processed
        counter = 0
        
        # Loop until all pages have been processed
        while True:
            # If all pages have been processed, break out of the loop
            if counter == 5: # To scrap 5 pages of pagination
                break
                
            try:
                # Find the next button
                next_button = browser.find_element(By.CLASS_NAME, "_1LKTO3")
                
                # If the next button is not enabled, break out of the loop
                if not next_button.is_enabled():
                    break
                    
                # Find all the link elements on the page
                link_elements = browser.find_elements(By.CLASS_NAME, "s1Q9rs")
                
                # Add the href attribute of each link element to the links list
                links.extend([link.get_attribute('href') for link in link_elements])
                
                # Wait for the next button to be clickable
                browser.implicitly_wait(25)
                
                # Click the next button
                next_button.click()
                
                # Increment the counter
                counter += 1
                
            # If an exception is raised, break out of the loop
            except:
                break
                
    # Close the webdriver
    browser.close()
    
    # Return the list of links
    return links
  
  
# url with base structure for scraping headphones
base_url='https://www.flipkart.com/search?q=headphones+boat&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&p%5B%5D=facets.brand%255B%255D%3D{}&page=1'
# List of Brand names to search for
brand_list=['boAt', 'Boult Audio', 'ZEBRONICS', 'Meyaar', 'Portronics', 'Noise', 'Wings', 'Skullcandy', 'PTron', 'Jabra']


# Calling the function to scrap all the product links of the brands above and storing it in a list
links=get_product_links(base_url,brand_list)

# Removing duplicate links
links=list(set(links))


def get_product_details():
    # Create an empty dictionary to store the product details
    details_dict={}
    
    # Try to find the product title and store it in the dictionary
    try:
        # Find the element that contains the product title using the XPATH selector
        title_element=browser.find_element(By.XPATH,'//span[@class="B_NuCI"]')
        # Extract the text content of the title element
        title=title_element.text
    except:
        # If the element is not found, set the title to "NaN"
        title= 'NaN'
    details_dict['Title']=title
    
    # Try to find the actual price and store it in the dictionary
    try:
        # Find the element that contains the actual price using the XPATH selector
        actual_price_element = browser.find_element(By.XPATH, '//div[@class="_3I9_wc _2p6lqe"]')
        # Extract the text content of the actual price element
        actual_price = actual_price_element.text
    except:
        # If the element is not found, set the actual price to "NaN"
        actual_price = 'NaN'
    details_dict['Actual_Price']=actual_price
    
    # Try to find the selling price and store it in the dictionary
    try:
        # Find the element that contains the selling price using the XPATH selector
        selling_price_element=browser.find_element(By.XPATH,'//div[@class="_30jeq3 _16Jk6d"]')
        # Extract the text content of the selling price element
        selling_price=selling_price_element.text
    except:
        # If the element is not found, set the selling price to "NaN"
        selling_price= 'NaN'
    details_dict['Selling_Price']=selling_price
    
    # Find the specification table using the XPATH selector
    spec_table = browser.find_element(By.XPATH, '//table[@class="_14cfVK"]')
    # Find all the rows in the specification table
    rows = spec_table.find_elements(By.XPATH, './/tr')
    
    # Try to extract the specification name and value for each row
    try:
        for row in rows:
            # Find the specification name element using the XPATH selector
            spec_name = row.find_element(By.XPATH, './/td[1][@class="_1hKmbr col col-3-12"]').text
            # Find the specification value element using the XPATH selector
            spec_value = row.find_element(By.XPATH, './/td[2][@class="URwL2w col col-9-12"]').text

            # Add the specification name and value to the dictionary
            details_dict[spec_name] = spec_value
    except NoSuchElementException:
        # If the element is not found, print "no specification" and continue with the next iteration
        print("no specification")
        pass

    # Return the dictionary that contains all the product details
    return details_dict
  
# Call the function for all the links
import pandas as pd
lst=[]
for link in links:
    try:
        browser = webdriver.Chrome()
        browser.get(link)
        lst.append(pd.DataFrame(get_product_details(),index=[0]))
    except:
        continue
df=pd.concat(lst,ignore_index=True)
df.reset_index(drop=True, inplace=True)

# Converting df to CSV
df.to_csv('flipkart_product_details.csv', index=False) 

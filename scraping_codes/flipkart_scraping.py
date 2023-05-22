
# Importing required libraries from selenium 
from selenium import webdriver
from selenium.webdriver.common.by import By

# Library to deal with the dataframes
import pandas as pd

# Importing exception handling libraries
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

# Defining a function that fetch product links of required brands
# Fetches product links of required brands from a given base URL.
# Args: base_url (str): The base URL to fetch product links from | brand_list (list): List of brands to fetch product links for.
# Returns: list: List of product links.

def get_product_links(base_url, brand_list):
    links = []
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode (without opening a browser window)
    
    browser = webdriver.Chrome(options=chrome_options)

    for brand in brand_list:
        url = base_url.format(brand)
        browser.get(url)
        # Counter to keep track of the number of pages processed
        counter = 0

        while True:
            if counter == 5: # To scrap 5 pages of pagination
                break

            try:
                next_button = browser.find_element(By.CLASS_NAME, "_1LKTO3")

                if not next_button.is_enabled():
                    break

                link_elements = browser.find_elements(By.CLASS_NAME, "s1Q9rs")
                links.extend([link.get_attribute('href') for link in link_elements])

                browser.implicitly_wait(25)
                next_button.click()
                counter += 1

            except:
                break

    browser.quit()
    return links
  
  
# url with base structure for scraping headphones
base_url='https://www.flipkart.com/search?q=headphones+boat&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&p%5B%5D=facets.brand%255B%255D%3D{}&page=1'
# List of Brand names to search for
brand_list=['boAt', 'SONY', 'ZEBRONICS', 'Meyaar', 'Portronics', 'Noise', 'Wings', 'Skullcandy', 'PTron', 'Jabra']


# Calling the function to scrap all the product links of the brands above and storing it in a list
links=get_product_links(base_url,brand_list)

# Removing duplicate links
links=list(set(links))

# Defining a function that returns a dataframe of product details of all products from a list of links
def get_product_details(links):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    browser = webdriver.Chrome(options=options)
    
    details_list = []
    
    for link in links:
        details_dict = {'product_link': link}
        
        try:
            browser.get(link)
            
            # Extract the product title
            title_element = browser.find_element(By.XPATH, '//span[@class="B_NuCI"]')
            title = title_element.text if title_element else 'NaN'
            details_dict['Title'] = title
            
            # Extract the actual price
            actual_price_element = browser.find_element(By.XPATH, '//div[@class="_3I9_wc _2p6lqe"]')
            actual_price = actual_price_element.text if actual_price_element else 'NaN'
            details_dict['Actual_Price'] = actual_price
            
            # Extract the selling price
            selling_price_element = browser.find_element(By.XPATH, '//div[@class="_30jeq3 _16Jk6d"]')
            selling_price = selling_price_element.text if selling_price_element else 'NaN'
            details_dict['Selling_Price'] = selling_price
            
            # Extract the specification details from the table
            spec_table = browser.find_element(By.XPATH, '//table[@class="_14cfVK"]')
            rows = spec_table.find_elements(By.XPATH, './/tr')
            
            for row in rows:
                # Extract the specification name
                spec_name_element = row.find_element(By.XPATH, './/td[1][@class="_1hKmbr col col-3-12"]')
                spec_name = spec_name_element.text if spec_name_element else 'NaN'
                
                # Extract the specification value
                spec_value_element = row.find_element(By.XPATH, './/td[2][@class="URwL2w col col-9-12"]')
                spec_value = spec_value_element.text if spec_value_element else 'NaN'
                
                # Add the specification to the details dictionary
                details_dict[spec_name] = spec_value
            
            # Append the details as a DataFrame to the list
            details_list.append(details_dict)
        
        except (NoSuchElementException, Exception) as e:
            print("Error occurred for link:", link)
            print(e)
            continue
        
    browser.quit()
    
    df = pd.DataFrame(details_list)
    
    return df

#calling function
df=get_product_details(links)
# Converting df to CSV
df.to_csv('flipkart_product_details.csv', index=False) 

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
                next_button = browser.find_element(By.CLASS_NAME, "s-pagination-item.s-pagination-next")
                
                # If the next button is not enabled, break out of the loop
                if not next_button.is_enabled():
                    break
                    
                # Find all the link elements on the page
                link_elements = browser.find_elements(By.CLASS_NAME, "a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal")
                
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


#url with base structure for scraping headphones
base_url='https://www.amazon.in/s?k=headphones&i=electronics&bbn=1388921031&rh=n%3A1388921031%2Cp_89%3A{}&dc&page=1&crid=26YCJ7VB7YLJ4&qid=1675167468&rnid=3837712031&sprefix=%2Caps%2C1567&ref=sr_pg_'
# List of Brand names to search for
brand_list=['boAt',  'Boult Audio', 'Mivi', 'JBL', 'ZEBRONICS',  'SONY', 'Ubon',  'Jabra', 'GoSale', 'Shop Reals']


#Calling the function to scrap all the product links of the brands above and storing it in a list
links=get_product_links(base_url,brand_list)

# Removing duplicate links
links=list(set(links))


def get_product_details(links):
    lst=[]
    browser = webdriver.Chrome()
    for link in links:
        details_dict={}
        try:
            
            browser.get(link)
            
        
    
            try:
                title_element=browser.find_element(By.XPATH,'//span[@class="a-size-large product-title-word-break"]')
                title=title_element.text
            except:
                title= 'NaN'
            details_dict['Title']=title
    
            try:
                actual_price_element = browser.find_element(By.XPATH, '//span[@class="a-price a-text-price"]')
                actual_price = actual_price_element.text
            except:
                actual_price = 'NaN'
            details_dict['Actual_Price']=actual_price
    
            try:
                selling_price_element = browser.find_element(By.XPATH, '//span[@class="a-price-whole"]')
                selling_price = selling_price_element.text
            except:
                selling_price = 'NaN'
            details_dict['Selling_Price']=selling_price
    
            spec_table = browser.find_element(By.XPATH, '//table[@class="a-normal a-spacing-micro"]')
            rows = spec_table.find_elements(By.XPATH, './/tr')
            try:
                for row in rows:
                    # Find the specification name and value
                    spec_name = row.find_element(By.XPATH, './/td[1]/span[@class="a-size-base a-text-bold"]').text
                    spec_value = row.find_element(By.XPATH, './/td[2]/span[@class="a-size-base po-break-word"]').text

                    # Add the specification name and value to the dictionary
                    details_dict[spec_name] = spec_value
            except NoSuchElementException:
                print("no specification")
                pass
            lst.append(pd.DataFrame(details_dict,index=[0]))
        except:
            continue
    browser.close()
    df=pd.concat(lst,ignore_index=True)
    df.reset_index(drop=True, inplace=True)

    # return the dataframe
    return df


#Converting df to CSV
df.to_csv('amazon_product_details.csv', index=False) 

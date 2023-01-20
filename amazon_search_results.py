#importing libraries

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd

#creating a function that scraps all links of search results from amazon
def get_amazon_links(site_link):
    browser = webdriver.Chrome()
    browser.get(site_link)
    links = []
    no_of_pages = int(browser.find_elements(By.CLASS_NAME,'s-pagination-item.s-pagination-disabled')[1].text) #to find total number of pages in pagination
    for _ in range(no_of_pages-1):
        link_elements = browser.find_elements(By.CLASS_NAME,"a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal") 
        links.extend([i.get_attribute('href') for i in link_elements])
        browser.implicitly_wait(10)
        browser.find_element(By.CLASS_NAME,"s-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator").click() #to navigate to next page in pagination
    browser.close()
    return links

site_link = 'https://www.amazon.in/s?k=headphones&crid=7ZAA2LLG9Y4V&sprefix=headphone%2Caps%2C234&ref=nb_sb_noss_2'

all_links = get_amazon_links(site_link) #calling the function

dictionary={'Links':all_links}
df = pd.DataFrame(dictionary)
df.to_csv('Amazon_links.csv', index=False) 


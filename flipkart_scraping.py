#importing libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
browser = webdriver.Chrome()

#Site link we are trying to scrape
browser.get('https://www.flipkart.com/search?q=Headphones&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off')

time.sleep(2)

#To locate all the results' names in the first page
elem1 = browser.find_elements(By.CLASS_NAME, 's1Q9rs')
#Putting headphones' names to a list
hp_names = [i.get_attribute('text') for i in elem1]

#To locate price of each item
elem2 = browser.find_elements(By.CLASS_NAME, '_30jeq3')
#Putting headphones' prices to a list
hp_prices = [i.text for i in elem2]

#To locate the ratings
elem3 = browser.find_elements(By.CLASS_NAME, '_3LWZlK')
#Putting headphones' ratings to a list
hp_ratings = [i.text for i in elem3]

#Printing all of them
print (hp_names)
print (hp_prices)
print (hp_ratings)          


#import Web Automation Module
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv

# Create a new instance of the Chrome driver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(r"C:\Users\USER\Downloads\chromedriver_win32 (2)\chromedriver",chrome_options=chrome_options)

# Navigate to the Amazon website
driver.get("https://www.amazon.com/s?k=headphones")

# Find all elements containing headphones' names, prices and images
name_elements = driver.find_elements(By.XPATH, '//span[@class="a-size-medium a-color-base a-text-normal"]')
price_elements = driver.find_elements(By.XPATH, '//span[@class="a-price-whole"]')
img_elements = driver.find_elements(By.XPATH, '//img[@class="s-image"]')

# Create an empty list to store the headphones' names, prices and images
headphones = []

# Iterate through the elements and extract the text
for i in range(len(name_elements)):
    name = name_elements[i].text
    price = price_elements[i].text
    img_url = img_elements[i].get_attribute("src")
    headphones.append([name, price, img_url])

# Write the headphones' names, prices and images to a CSV file
with open('headphones.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Name', 'Price', 'Image'])
    writer.writerows(headphones)


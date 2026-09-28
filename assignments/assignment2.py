from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

driver.get("file:///C:/Users/anand/OneDrive/Desktop/selenium%20assignment/assignment1.html")

# Find all links
links = driver.find_elements(By.TAG_NAME, "a")

# Print total number of links
print("Total links:", len(links))

# Print text of every link
for link in links:
    print("Link:", link.text)

driver.quit()
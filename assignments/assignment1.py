from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

driver.get("file:///C:/Users/anand/OneDrive/Desktop/selenium%20assignment/assignment1.html")

# 1. Locate using ID
username = driver.find_element(By.ID, "username")
print("Username field found")

# 2. Locate using NAME
password = driver.find_element(By.NAME, "password")
print("Password field found")

# 3. Locate using TAG_NAME
button = driver.find_element(By.TAG_NAME, "button")
print("Login button found")

# 4. Locate using LINK_TEXT
link = driver.find_element(By.LINK_TEXT, "Forgot Password")
print("Forgot Password link found")

# 5. Locate using CLASS_NAME
email = driver.find_element(By.CLASS_NAME, "email-field")
print("Email field found")

driver.quit()
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

driver.get("file:///C:/Users/anand/OneDrive/Desktop/selenium%20assignment/assignment1.html")

# 1. Starts with "user_"
element1 = driver.find_element(
    By.CSS_SELECTOR,
    '[id^="user_"]'
)
print("Starts with user_:", element1.get_attribute("id"))

# 2. Contains "user"
element2 = driver.find_element(
    By.CSS_SELECTOR,
    '[id*="user"]'
)
print("Contains user:", element2.get_attribute("id"))

# 3. Ends with "_field"
element3 = driver.find_element(
    By.CSS_SELECTOR,
    '[id$="_field"]'
)
print("Ends with _field:", element3.get_attribute("id"))

driver.quit()
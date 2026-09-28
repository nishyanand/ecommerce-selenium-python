from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

driver.get("file:///C:/Users/anand/OneDrive/Desktop/selenium%20assignment/assignment1.html")

# Locate button inside the div using CSS child selector
button = driver.find_element(
    By.CSS_SELECTOR,
    "#login-container > button"
)

print("Child button found:", button.text)

# Interact with the child element
button.click()

print("Button clicked successfully")

driver.quit()
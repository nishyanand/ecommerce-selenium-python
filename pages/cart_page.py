"""
cart_page.py
Page Object representing the TutorialsNinja Shopping Cart Page.

Encapsulates:
- Cart table line item locators (product name, model, quantity, unit price, total price)
- Actions: reading line items, modifying quantity, submitting updates, querying alerts
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CartPage:
    """
    Page Object Model class for the Shopping Cart Page.
    """

    # -------------------------------------------------------------
    # 1. PAGE LOCATORS
    # -------------------------------------------------------------
    CART_TABLE = (By.CSS_SELECTOR, "div#content form table.table-bordered")
    PRODUCT_NAME_LINK = (By.XPATH, "//div[@id='content']//form//tbody/tr/td[2]/a")
    MODEL_CELL = (By.XPATH, "//div[@id='content']//form//tbody/tr/td[3]")
    QUANTITY_INPUT = (By.XPATH, "//div[@id='content']//form//tbody/tr/td[4]//input")
    UPDATE_BUTTON = (By.XPATH, "//div[@id='content']//form//tbody/tr/td[4]//button[@data-original-title='Update' or @type='submit']")
    UNIT_PRICE_CELL = (By.XPATH, "//div[@id='content']//form//tbody/tr/td[5]")
    TOTAL_PRICE_CELL = (By.XPATH, "//div[@id='content']//form//tbody/tr/td[6]")
    SUCCESS_ALERT = (By.CSS_SELECTOR, "div.alert-success")
    EMPTY_CART_MESSAGE = (By.XPATH, "//div[@id='content']//p[contains(text(), 'Your shopping cart is empty!')]")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # -------------------------------------------------------------
    # 2. NAVIGATION & STATUS
    # -------------------------------------------------------------
    def open(self, base_url="https://tutorialsninja.com/demo/"):
        """Navigates directly to the shopping cart page."""
        cart_url = f"{base_url.rstrip('/')}/index.php?route=checkout/cart"
        logger.info("Opening Cart page")
        self.driver.get(cart_url)

    def is_cart_table_displayed(self):
        """Returns True if the cart table containing items is displayed."""
        try:
            table = self.wait.until(EC.presence_of_element_located(self.CART_TABLE))
            return table.is_displayed()
        except TimeoutException:
            return False

    # -------------------------------------------------------------
    # 3. LINE ITEM QUERIES
    # -------------------------------------------------------------
    def get_product_name(self):
        """Returns the product title of the first line item in the cart."""
        elem = self.wait.until(EC.visibility_of_element_located(self.PRODUCT_NAME_LINK))
        return elem.text.strip()

    def get_model(self):
        """Returns the product model code from column 3 (e.g. 'Product 16')."""
        elem = self.wait.until(EC.visibility_of_element_located(self.MODEL_CELL))
        return elem.text.strip()

    def get_quantity(self):
        """Returns the current quantity value from the input field."""
        elem = self.wait.until(EC.visibility_of_element_located(self.QUANTITY_INPUT))
        return elem.get_attribute("value").strip()

    def get_unit_price(self):
        """Returns the unit price text (e.g. '$602.00')."""
        elem = self.wait.until(EC.visibility_of_element_located(self.UNIT_PRICE_CELL))
        return elem.text.strip()

    def get_total_price(self):
        """Returns the total price text for the line item (e.g. '$1,204.00')."""
        elem = self.wait.until(EC.visibility_of_element_located(self.TOTAL_PRICE_CELL))
        return elem.text.strip()

    # -------------------------------------------------------------
    # 4. CART ACTIONS
    # -------------------------------------------------------------
    def update_quantity(self, new_quantity):
        """
        Updates the product quantity and clicks the blue update button.
        Waits for the recalculation success banner.
        """
        logger.info(f"Updating quantity to {new_quantity}")
        # 1. Clear and enter new quantity
        qty_input = self.wait.until(EC.visibility_of_element_located(self.QUANTITY_INPUT))
        qty_input.clear()
        qty_input.send_keys(str(new_quantity))

        # 2. Click update button
        btn = self.wait.until(EC.element_to_be_clickable(self.UPDATE_BUTTON))
        btn.click()

        # 3. Wait for success alert confirming modification
        self.wait.until(EC.visibility_of_element_located(self.SUCCESS_ALERT))

    def get_update_success_message(self):
        """Returns the text of the modification success alert banner."""
        alert = self.wait.until(EC.visibility_of_element_located(self.SUCCESS_ALERT))
        return alert.text.strip()

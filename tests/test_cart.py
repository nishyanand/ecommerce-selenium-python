import pytest
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from utils.test_data_reader import load_test_data

def test_tc004_add_product_to_cart(driver):
    """
    TC004 — Add Product To Cart
    Objective: Verify that a selected product can be added to the cart and appears in the cart page.
    """
    product_data = load_test_data("product")
    product_name = product_data["name"]
    
    # 1. Search product
    home_page = HomePage(driver)
    home_page.open()
    home_page.search_product(product_name)
    
    # 2. Open product details
    home_page.select_product(product_name)
    
    # 3. Verify product title
    product_page = ProductPage(driver)
    assert product_page.get_product_title() == product_name, (
        f"Product title on details page mismatch! Expected '{product_name}'"
    )
    
    # 4 & 5. Add to cart & verify success alert
    product_page.click_add_to_cart()
    success_msg = product_page.get_success_message()
    expected_msg_snippet = f"Success: You have added {product_name} to your shopping cart!"
    assert expected_msg_snippet in success_msg, (
        f"Expected snippet '{expected_msg_snippet}' not found in '{success_msg}'"
    )
    
    # 6. Navigate to Cart via alert link
    product_page.go_to_cart_via_alert()
    
    # 7. Verify product is in cart
    cart_page = CartPage(driver)
    assert cart_page.is_cart_table_displayed(), "Shopping cart table is not displayed!"
    actual_cart_item = cart_page.get_product_name()
    assert actual_cart_item == product_name, (
        f"Product in cart mismatch! Expected '{product_name}', got '{actual_cart_item}'"
    )

def test_tc005_update_quantity(driver):
    """
    TC005 — Update Quantity
    Objective: Verify that the product quantity can be successfully updated in the cart.
    """
    product_data = load_test_data("product")
    product_name = product_data["name"]
    initial_expected_qty = product_data["initial_quantity"]
    new_qty = product_data["updated_quantity"]
    
    # 1. Search and open product
    home_page = HomePage(driver)
    home_page.open()
    home_page.search_product(product_name)
    home_page.select_product(product_name)
    
    # 2. Add to cart & navigate
    product_page = ProductPage(driver)
    product_page.click_add_to_cart()
    product_page.go_to_cart_via_alert()
    
    cart_page = CartPage(driver)
    assert cart_page.is_cart_table_displayed(), "Cart table is not displayed!"
    
    # 3. Check initial quantity
    initial_qty = cart_page.get_quantity()
    assert initial_qty == initial_expected_qty, (
        f"Expected initial quantity '{initial_expected_qty}', found '{initial_qty}'"
    )
    
    # 4. Update quantity
    cart_page.update_quantity(new_qty)
    
    # 5. Verify update success banner
    update_msg = cart_page.get_update_success_message()
    expected_msg = "Success: You have modified your shopping cart!"
    assert expected_msg in update_msg, (
        f"Expected update message '{expected_msg}' not found in '{update_msg}'"
    )
    
    # 6. Verify updated quantity in the input field
    updated_qty = cart_page.get_quantity()
    assert updated_qty == new_qty, (
        f"Updated quantity mismatch! Expected '{new_qty}', got '{updated_qty}'"
    )

def test_tc006_cart_verification(driver):
    """
    TC006 — Cart Verification
    Objective: Verify complete line-item integrity and financial calculation in the shopping cart.
    """
    product_data = load_test_data("product")
    product_name = product_data["name"]
    expected_model = product_data["model"]
    expected_unit_price = product_data["unit_price"]
    expected_initial_total = product_data["initial_total"]
    updated_quantity = product_data["updated_quantity"]
    expected_recalculated_total = product_data["updated_total"]
    
    # 1. Search and open product
    home_page = HomePage(driver)
    home_page.open()
    home_page.search_product(product_name)
    home_page.select_product(product_name)
    
    # 2. Add to cart & open cart
    product_page = ProductPage(driver)
    product_page.click_add_to_cart()
    product_page.go_to_cart_via_alert()
    
    cart_page = CartPage(driver)
    
    # 3. Assert cart presence
    assert cart_page.is_cart_table_displayed(), "Shopping cart table is not displayed!"
    
    # 4. Assert Product Name
    actual_product = cart_page.get_product_name()
    assert actual_product == product_name, (
        f"Product name mismatch! Expected '{product_name}', got '{actual_product}'"
    )
    
    # 5. Assert Product Model
    actual_model = cart_page.get_model()
    assert actual_model == expected_model, (
        f"Model mismatch! Expected '{expected_model}', got '{actual_model}'"
    )
    
    # 6. Assert Initial Quantity
    actual_qty = cart_page.get_quantity()
    assert actual_qty == product_data["initial_quantity"], (
        f"Expected quantity '{product_data['initial_quantity']}', got '{actual_qty}'"
    )
    
    # 7. Assert Unit Price
    actual_unit_price = cart_page.get_unit_price()
    assert actual_unit_price == expected_unit_price, (
        f"Unit price mismatch! Expected '{expected_unit_price}', got '{actual_unit_price}'"
    )
    
    # 8. Assert Line Total
    actual_total = cart_page.get_total_price()
    assert actual_total == expected_initial_total, (
        f"Initial total mismatch! Expected '{expected_initial_total}', got '{actual_total}'"
    )
    
    # 9. Update quantity and verify recalculated line total
    cart_page.update_quantity(updated_quantity)
    assert cart_page.get_quantity() == updated_quantity, f"Quantity failed to update to {updated_quantity}!"
    
    recalculated_total = cart_page.get_total_price()
    assert recalculated_total == expected_recalculated_total, (
        f"Recalculated total mismatch! Expected '{expected_recalculated_total}', got '{recalculated_total}'"
    )
    
    # Milestone Screenshot
    from utils.screenshot_helper import take_screenshot
    take_screenshot(driver, "cart_verification_success")



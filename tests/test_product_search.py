"""
test_product_search.py
Test Cases for Product Search:
- TC003: Product Search (Valid & Invalid cases)
"""

import pytest
from pages.home_page import HomePage
from utils.test_data_reader import load_test_data

def test_tc003_product_search_valid(driver):
    """
    TC003 — Product Search (Positive)
    Objective: Verify that searching for a valid product returns matching results.
    """
    product_data = load_test_data("product")
    product_name = product_data["name"]

    home_page = HomePage(driver)
    home_page.open()
    home_page.search_product(product_name)
    
    # Assert at least one product is returned
    count = home_page.get_search_results_count()
    assert count > 0, f"Expected at least 1 search result, but got {count}!"
    
    # Assert specific product is displayed
    assert home_page.is_product_in_results(product_name), (
        f"Product '{product_name}' was not found in the search results list!"
    )
    
    # Milestone Screenshot
    from utils.screenshot_helper import take_screenshot
    take_screenshot(driver, "product_search_success")

def test_tc003_product_search_nonexistent(driver):
    """
    TC003 — Product Search (Negative)
    Objective: Verify that searching for a non-existent item displays the zero-results message.
    """
    nonexistent_data = load_test_data("nonexistent_product")
    query = nonexistent_data["name"]
    expected_msg = nonexistent_data["expected_message"]

    home_page = HomePage(driver)
    home_page.open()
    home_page.search_product(query)
    
    count = home_page.get_search_results_count()
    assert count == 0, f"Expected 0 results for non-existent product, found {count}!"
    assert home_page.has_no_product_message(), (
        f"Zero-results notification message '{expected_msg}' was not displayed!"
    )

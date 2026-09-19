"""
test_login.py
Test Cases for User Authentication:
- TC001: Valid Login
- TC002: Invalid Login
"""

import pytest
from pages.login_page import LoginPage
from utils.test_data_reader import load_test_data

def test_tc001_valid_login(driver):
    """
    TC001 — Valid Login
    Objective: Verify that a valid registered user can successfully log in.
    """
    valid_data = load_test_data("valid_user")
    
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(valid_data["email"], valid_data["password"])
    
    assert login_page.is_logged_in(), "Login failed: 'My Account' dashboard was not displayed!"
    
    # Milestone Screenshot: Evidence of successful login
    from utils.screenshot_helper import take_screenshot
    take_screenshot(driver, "login_success")

def test_tc002_invalid_login(driver):
    """
    TC002 — Invalid Login
    Objective: Verify that an appropriate error banner appears for invalid credentials.
    """
    invalid_data = load_test_data("invalid_user")
    
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(invalid_data["email"], invalid_data["password"])
    
    error_message = login_page.get_error_message()
    expected_error = invalid_data["expected_error"]
    
    assert expected_error in error_message, (
        f"Expected error message '{expected_error}' not found in actual: '{error_message}'"
    )

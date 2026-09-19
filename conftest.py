"""
conftest.py
PyTest configuration and shared fixtures for the test suite.

Provides:
- driver: Shared fixture to initialize and quit Chrome WebDriver cleanly for each test.
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from utils.config_reader import is_headless
from utils.logger import get_logger

@pytest.fixture
def driver():
    """
    PyTest fixture for managing WebDriver lifecycle.
    - Setup: Reads configuration (e.g., headless mode), launches Chrome, and maximizes viewport.
    - Yield: Hands the driver object to the requesting test function.
    - Teardown: Calls driver.quit() after test execution completes (even on failure).
    """
    chrome_options = Options()
    if is_headless():
        chrome_options.add_argument("--headless=new")
        
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver_instance = webdriver.Chrome(options=chrome_options)
    driver_instance.maximize_window()

    yield driver_instance

    # Teardown guarantees browser process termination
    driver_instance.quit()

# Logging fixtures

@pytest.fixture(scope="session", autouse=True)
def setup_logging():
    logger = get_logger("test_session")
    logger.info("Test session started")
    yield
    logger.info("Test session finished")

@pytest.fixture(autouse=True)
def log_test(request):
    logger = get_logger(__name__)
    logger.info(f"Starting test: {request.node.name}")
    yield
    logger.info(f"Finished test: {request.node.name}")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    PyTest hook wrapper executed for each phase of a test (setup, call, teardown).
    If a test fails during execution ('call' phase), it automatically captures
    a failure screenshot using the active WebDriver instance and attaches it to the report.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            from utils.screenshot_helper import take_screenshot
            screenshot_path = take_screenshot(driver, f"FAILED_{item.name}")
            print(f"\n[FAILURE HOOK] Automated failure screenshot saved to: {screenshot_path}")

            # Attach to pytest-html report if plugin is active
            html_plugin = item.config.pluginmanager.getplugin("html")
            if html_plugin:
                extras = getattr(report, "extras", [])
                extras.append(html_plugin.extras.image(screenshot_path))
                report.extras = extras

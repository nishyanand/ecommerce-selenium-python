# E‑Commerce Selenium Automation Demo

## Overview
A lightweight Selenium automation suite that validates key e‑commerce workflows on the public **TutorialsNinja** demo site.

## Business Scenario
The demo site mimics a small online store. The tests automate a typical user journey: login, product search, add‑to‑cart, update quantity, and cart verification.

## Objectives
- Demonstrate Page Object Model (POM) in Python.
- Show reliable handling of a cookie‑consent banner.
- Capture screenshots on failure and generate an HTML report.
- Provide clear logging for debugging.

## Technologies Used
- **Python 3.14**
- **Selenium WebDriver**
- **pytest** (testing framework)
- **pytest‑html** (HTML report generation)
- Standard **logging** module

## Project Structure
```
ecommerce-selenium-python/
├─ pages/                # Page Object Model classes
│   ├─ home_page.py
│   ├─ login_page.py
│   ├─ product_page.py
│   └─ cart_page.py
├─ tests/                # Test cases (7 total)
│   ├─ test_login.py
│   ├─ test_product_search.py
│   └─ test_cart.py
├─ utils/                # Helper modules (logger, config, cookie handler, screenshot helper)
│   ├─ logger.py
│   ├─ config_reader.py
│   ├─ cookie_handler.py
│   └─ screenshot_helper.py
├─ conftest.py           # pytest fixtures & screenshot hook
├─ requirements.txt
├─ pytest.ini            # pytest‑html configuration
├─ .gitignore            # ignores reports/, screenshots/, logs/
└─ README.md             # <--- this file
```

## Automation Workflow
1. **driver fixture** – creates a Chrome WebDriver (headless configurable) and quits after each test.
2. **HomePage.open()** – navigates to the base URL, dismisses the cookie banner, and waits for the search box.
3. Test‑specific page objects perform actions (login, search, add to cart, update quantity).
4. On test failure the `pytest_runtest_makereport` hook captures a screenshot and attaches it to the HTML report.

## Test Cases Covered
| Test | Scenario |
|------|----------|
| `test_tc001_valid_login` | Successful login with valid credentials |
| `test_tc002_invalid_login` | Login failure with wrong password |
| `test_tc003_product_search_valid` | Search for an existing product |
| `test_tc003_product_search_nonexistent` | Search for a non‑existent product |
| `test_tc004_add_product_to_cart` | Add a product to the cart |
| `test_tc005_update_quantity` | Change the quantity of a cart item |
| `test_tc006_cart_verification` | Verify totals and quantities in the cart |

## Test Data Approach
Static credentials and product names are stored in the **test_data/** directory (JSON files). The tests read them via the `utils.config_reader` helper.

## Selenium / POM Approach
- Each page is a class exposing **locators** and **action methods**.
- Explicit waits (`WebDriverWait`) protect against timing issues.
- No hard‑coded sleeps; all interactions are resilient.

## Cookie / Popup Handling
`utils/cookie_handler.py` provides `dismiss_cookie_banner(driver)` which uses the verified DOM selector for the TutorialsNinja consent banner and clicks the **Accept** button before any further actions.

## Screenshot Handling
The `pytest_runtest_makereport` hook in `conftest.py` calls `utils/screenshot_helper.py` to capture a PNG when a test fails. Images are saved under **screenshots/** and automatically embedded in the HTML report.

## HTML Reporting with pytest‑html
Running `pytest -v` generates **reports/report.html** (configured in `pytest.ini`). The report includes:
- Test outcome summary
- Embedded failure screenshots
- Execution timestamps

## Logging
A central logger (`utils/logger.py`) writes INFO‑level entries to **logs/test_execution.log** and also streams to the console. Session‑level and per‑test logs are added via fixtures in `conftest.py`.

## Setup / Prerequisites
- Python 3.14+ installed
- Google Chrome browser
- ChromeDriver matching your Chrome version (the script uses the default driver on PATH)
- (Optional) virtual environment for isolation

## Installation Steps
```bash
# 1. Clone the repository
git clone <repo‑url>
cd ecommerce-selenium-python

# 2. Create and activate a virtual environment (recommended)
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

## How to Run the Tests
```bash
# Run all tests and generate the HTML report
pytest -v

# Open the report after execution (Windows example)
start reports\report.html
```

## Where to Find Artifacts
- **HTML report** – `reports/report.html`
- **Failure screenshots** – `screenshots/` (populated only on failures)
- **Execution logs** – `logs/test_execution.log`

## Example Test Execution
```
$ pytest -v
============================= test session starts =============================
platform win32 -- Python 3.14.7, pytest-9.1.1, pluggy-1.6.0
...
collected 7 items

tests/test_login.py::test_tc001_valid_login PASSED
...
======================== 7 passed in 79.01s =========================
```
The report file and logs are created as described above.

## Expected Result
All seven tests pass, the HTML report displays a green pass list, and the log file contains timestamps and INFO messages for each test.

## Interview Discussion Points
- Why a **single logger** instance is preferred over per‑module loggers.
- Benefits of **POM** for maintainability.
- How the **cookie‑banner handling** avoids flaky tests.
- The role of the **pytest‑html hook** for failure evidence.
- Choices around **headless vs. headed** execution controlled via `config/config.json`.

## Limitations / Scope
- Limited to the public TutorialsNinja demo site; no private application support.
- No parallel test execution or Selenium Grid usage.
- No CI/CD pipeline – tests are executed locally.
- Test data is static; no data‑driven generation.
- Logging is simple INFO level; no advanced rotation or external aggregation.

---
*The README is placed at the repository root as `README.md`.*

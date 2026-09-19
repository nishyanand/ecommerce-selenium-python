from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

_TIMEOUT = 5

def _find_accept_button(container):
    """Return a button inside *container* that looks like an accept/agree button.
    Raises NoSuchElementException if none is found.
    """
    accept_phrases = ["accept", "agree", "got it", "allow", "dismiss", "close"]
    for phrase in accept_phrases:
        try:
            btn = container.find_element(
                By.XPATH,
                f".//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{phrase.lower()}')]"
            )
            return btn
        except NoSuchElementException:
            continue
    raise NoSuchElementException("Accept button not found in cookie banner")

def dismiss_cookie_banner(driver) -> bool:
    """Detect and dismiss the cookie‑consent banner.

    Args:
        driver: Selenium WebDriver instance that has already navigated to the target page.

    Returns:
        bool: True if a banner was found and dismissed, False otherwise.
    """
    try:
        banner = WebDriverWait(driver, _TIMEOUT).until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//*[contains(translate(@id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'cookie') or contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'cookie')]"
                )
            )
        )
        btn = _find_accept_button(banner)
        btn.click()
        # Ensure the banner disappears before proceeding
        try:
            WebDriverWait(driver, _TIMEOUT).until_not(
                EC.presence_of_element_located(
                    (By.XPATH, "//*[contains(translate(@id, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'cookie') or contains(translate(@class, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'cookie')]")
                )
            )
        except TimeoutException:
            pass
        return True
    except (TimeoutException, NoSuchElementException):
        return False

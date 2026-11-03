"""A3 - Cuộn danh sách & chụp màn hình
(8.3 Scroll, 8.7 Screenshot, 7.19 Remote WebDriver, 7.20 WebElement)."""
import os
from selenium.webdriver.support import expected_conditions as EC

from helpers import ITEM, SCREENSHOT_DIR, scroll_to_text, swipe_up, titles, screenshot


def test_scroll_uiscrollable_and_screenshot(driver, wait):
    wait.until(EC.visibility_of_element_located(ITEM))
    target = scroll_to_text(driver, "Test.allTheThings")  # UiScrollable
    assert target.is_displayed()

    path = screenshot(driver, "products_scrolled.png")  # 8.7: save_screenshot
    assert os.path.getsize(path) > 0


def test_scroll_gesture(driver, wait):
    wait.until(EC.visibility_of_element_located(ITEM))
    before = titles(driver)
    swipe_up(driver)  # execute_script("mobile: scrollGesture", {...})
    after = titles(driver)
    assert before != after, "Danh sách không thay đổi sau khi cuộn"


def test_element_screenshot(driver, wait):
    """7.20 WebElement: element.screenshot(filename)."""
    item = wait.until(EC.visibility_of_element_located(ITEM))
    path = os.path.join(SCREENSHOT_DIR, "first_item.png")
    assert item.screenshot(path)
    assert os.path.exists(path)

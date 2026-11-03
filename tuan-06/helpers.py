"""Hàm dùng chung + locator cho bài tuần 06 (Swag Labs / Sauce Labs My Demo App - Android)."""
import os
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC

SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "anh")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# ---------- Locators (kiểm tra lại bằng Appium Inspector nếu app khác) ----------
ITEM = (AppiumBy.ACCESSIBILITY_ID, "store item")
ITEM_TITLE = (AppiumBy.ACCESSIBILITY_ID, "store item text")
ITEM_PRICE = (AppiumBy.ACCESSIBILITY_ID, "store item price")
SORT_BTN = (AppiumBy.ACCESSIBILITY_ID, "sort button")
SORT_NAME_ASC = (AppiumBy.ACCESSIBILITY_ID, "nameAsc")
SORT_NAME_DESC = (AppiumBy.ACCESSIBILITY_ID, "nameDesc")
SORT_PRICE_ASC = (AppiumBy.ACCESSIBILITY_ID, "priceAsc")
SORT_PRICE_DESC = (AppiumBy.ACCESSIBILITY_ID, "priceDesc")
ADD_TO_CART = (AppiumBy.ACCESSIBILITY_ID, "Add To Cart button")
CART_ICON = (AppiumBy.ACCESSIBILITY_ID, "cart badge")
CART_ITEM = (AppiumBy.ACCESSIBILITY_ID, "product row")
REMOVE_ITEM = (AppiumBy.ACCESSIBILITY_ID, "remove item")
ANDROID_OK_BUTTON = (AppiumBy.ID, "android:id/button1")


def titles(driver):
    """Danh sách tên sản phẩm đang hiển thị."""
    return [e.text for e in driver.find_elements(*ITEM_TITLE)]


def prices(driver):
    """Danh sách giá (float) đang hiển thị."""
    return [float(e.text.replace("$", "").strip()) for e in driver.find_elements(*ITEM_PRICE)]


def choose_sort(driver, wait, option):
    """Mở menu sắp xếp rồi chọn một tuỳ chọn (explicit wait)."""
    wait.until(EC.element_to_be_clickable(SORT_BTN)).click()
    wait.until(EC.visibility_of_element_located(option)).click()


def scroll_to_text(driver, text):
    """Cuộn bằng UiScrollable tới phần tử chứa text."""
    return driver.find_element(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiScrollable(new UiSelector().scrollable(true))'
        f'.scrollIntoView(new UiSelector().textContains("{text}"))',
    )


def swipe_up(driver):
    """Cuộn danh sách bằng execute_script (mobile: scrollGesture)."""
    size = driver.get_window_size()
    driver.execute_script(
        "mobile: scrollGesture",
        {
            "left": 100, "top": 400,
            "width": size["width"] - 200, "height": size["height"] // 2,
            "direction": "down", "percent": 0.8,
        },
    )


def screenshot(driver, name):
    """Chụp toàn màn hình vào thư mục anh/ và trả về đường dẫn."""
    path = os.path.join(SCREENSHOT_DIR, name)
    driver.save_screenshot(path)
    return path

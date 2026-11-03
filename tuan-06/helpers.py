"""Hàm dùng chung + locator cho bài tuần 06 (Sauce Labs My Demo App - Android)."""
import os
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC

SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "anh")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# ---------- Locators (đã xác minh thực tế trên com.saucelabs.mydemoapp.android) ----------
ITEM = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/productIV")
ITEM_TITLE = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/titleTV")
ITEM_PRICE = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/priceTV")
SORT_BTN = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/sortIV")
SORT_NAME_ASC = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/nameAscCL")
SORT_NAME_DESC = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/nameDesCL")
SORT_PRICE_ASC = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/priceAscCL")
SORT_PRICE_DESC = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/priceDesCL")
ADD_TO_CART = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/cartBt")
CART_ICON = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/cartRL")
CART_ITEM = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/removeBt")
REMOVE_ITEM = (AppiumBy.ID, "com.saucelabs.mydemoapp.android:id/removeBt")
ANDROID_OK_BUTTON = (AppiumBy.ID, "android:id/button1")


def titles(driver):
    """Danh sách tên sản phẩm đang hiển thị."""
    return [e.text for e in driver.find_elements(*ITEM_TITLE) if e.text]


def prices(driver):
    """Danh sách giá (float) đang hiển thị."""
    res = []
    for e in driver.find_elements(*ITEM_PRICE):
        t = e.text.replace("$", "").replace(",", ".").strip()
        if t:
            try:
                res.append(float(t))
            except ValueError:
                pass
    return res


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

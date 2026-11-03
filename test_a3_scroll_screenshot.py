"""
Bài kiểm thử A3: Cuộn danh sách & Chụp màn hình (Swag Labs Android App)

Yêu cầu thực hiện:
1. Mở Swag Labs, đăng nhập.
2. Chờ màn hình PRODUCTS xuất hiện.
3. Chụp màn hình trước khi cuộn (lưu thư mục anh/).
4. Cuộn xuống danh sách sản phẩm (UiScrollable scrollIntoView / scrollForward).
5. Kiểm tra sản phẩm ở phía dưới danh sách đã xuất hiện.
6. Chụp màn hình sau khi cuộn (lưu thư mục anh/).
7. Luôn đóng phiên bằng driver.quit() trong finally.
"""

import os
import subprocess
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Cấu hình thiết bị & Appium Server
APPIUM_SERVER = "http://127.0.0.1:4723"
DEVICE_NAME = "ATLSVB4103012319"
APP_PACKAGE = "com.swaglabsmobileapp"
APP_ACTIVITY = "com.swaglabsmobileapp.MainActivity"
WAIT_TIMEOUT = 15

# Tài khoản đăng nhập
VALID_USERNAME = "standard_user"
VALID_PASSWORD = "secret_sauce"

# Thư mục lưu ảnh bằng chứng
EVIDENCE_DIR = os.path.join(os.path.dirname(__file__), "anh")
os.makedirs(EVIDENCE_DIR, exist_ok=True)


@pytest.fixture(autouse=True)
def clean_app_environment():
    """Làm sạch trạng thái ứng dụng trước và sau khi chạy test để cách ly môi trường."""
    subprocess.run(["adb", "shell", "pm", "clear", APP_PACKAGE], check=True, capture_output=True)
    yield
    subprocess.run(["adb", "shell", "pm", "clear", APP_PACKAGE], capture_output=True)


def create_driver():
    """Khởi tạo phiên Remote WebDriver với Appium."""
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = DEVICE_NAME
    options.app_package = APP_PACKAGE
    options.app_activity = APP_ACTIVITY
    options.no_reset = True
    return webdriver.Remote(APPIUM_SERVER, options=options)


def login(driver, username, password):
    """Thực hiện đăng nhập vào Swag Labs."""
    wait = WebDriverWait(driver, WAIT_TIMEOUT)
    # Nhập Username
    user_elem = wait.until(EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, "test-Username")))
    user_elem.clear()
    user_elem.send_keys(username)

    # Nhập Password
    pwd_elem = wait.until(EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, "test-Password")))
    pwd_elem.clear()
    pwd_elem.send_keys(password)

    # Bấm LOGIN
    login_btn = wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "test-LOGIN")))
    login_btn.click()


def test_a3_scroll_and_screenshot():
    """
    Test Case A3:
    - Đăng nhập -> Vào màn PRODUCTS
    - Chụp màn hình trước khi cuộn
    - Cuộn xuống tìm sản phẩm ở dưới cùng ('Test.allTheThings() T-Shirt (Red)')
    - Xác minh sản phẩm xuất hiện
    - Chụp màn hình sau khi cuộn
    """
    driver = create_driver()
    try:
        wait = WebDriverWait(driver, WAIT_TIMEOUT)

        # Bước 1: Đăng nhập
        login(driver, VALID_USERNAME, VALID_PASSWORD)

        # Bước 2: Chờ màn hình PRODUCTS xuất hiện
        products_title = wait.until(
            EC.visibility_of_element_located((AppiumBy.XPATH, "//*[@text='PRODUCTS']"))
        )
        assert products_title.is_displayed(), "Không thấy màn hình PRODUCTS sau khi đăng nhập"

        # Bước 3: Chụp màn hình TRƯỚC KHI CUỘN
        before_scroll_path = os.path.join(EVIDENCE_DIR, "a3_truoc_cuon.png")
        saved_before = driver.save_screenshot(before_scroll_path)
        assert saved_before, f"Lưu ảnh trước khi cuộn thất bại tại: {before_scroll_path}"
        assert os.path.exists(before_scroll_path), "File ảnh trước khi cuộn không tồn tại"

        # Bước 4: Cuộn xuống danh sách sản phẩm bằng UiScrollable (native Android gesture)
        # Tìm sản phẩm ở cuối danh sách: 'Test.allTheThings() T-Shirt (Red)'
        target_product_text = "Test.allTheThings() T-Shirt (Red)"
        scroll_command = (
            f'new UiScrollable(new UiSelector().scrollable(true))'
            f'.scrollIntoView(new UiSelector().text("{target_product_text}"))'
        )

        bottom_product = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, scroll_command)

        # Bước 5: Kiểm tra sản phẩm phía dưới đã thực sự hiển thị
        assert bottom_product.is_displayed(), (
            f"Sản phẩm '{target_product_text}' không hiển thị sau khi cuộn"
        )
        assert bottom_product.text == target_product_text, "Tên sản phẩm không khớp"

        # Bước 6: Chụp màn hình SAU KHI CUỘN
        after_scroll_path = os.path.join(EVIDENCE_DIR, "a3_sau_cuon.png")
        saved_after = driver.save_screenshot(after_scroll_path)
        assert saved_after, f"Lưu ảnh sau khi cuộn thất bại tại: {after_scroll_path}"
        assert os.path.exists(after_scroll_path), "File ảnh sau khi cuộn không tồn tại"

    finally:
        # Bước 7: Đóng phiên kiểm thử và giải phóng tài nguyên
        driver.quit()

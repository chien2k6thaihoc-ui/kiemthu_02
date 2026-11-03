"""
Bài kiểm thử A4: Phiên Appium (Remote WebDriver) & Menu (Swag Labs Android App)

Yêu cầu thực hiện:
1. Khai báo cấu hình Android: platformName, automationName, thiết bị, package và activity.
2. Tạo phiên kết nối bằng webdriver.Remote(...).
3. Đăng nhập và kiểm tra màn hình PRODUCTS.
4. Mở menu, kiểm tra menu hiển thị.
5. Chọn một mục menu, chẳng hạn Logout, rồi kiểm tra ứng dụng trở về màn hình đăng nhập.
6. Đóng phiên bằng driver.quit() trong finally.
"""

import os
import subprocess
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1. Cấu hình kết nối Android & Appium Server
APPIUM_SERVER = "http://127.0.0.1:4723"
DEVICE_NAME = "ATLSVB4103012319"
APP_PACKAGE = "com.swaglabsmobileapp"
APP_ACTIVITY = "com.swaglabsmobileapp.MainActivity"
WAIT_TIMEOUT = 15

# Thông tin tài khoản kiểm thử
VALID_USERNAME = "standard_user"
VALID_PASSWORD = "secret_sauce"

# Thư mục lưu bằng chứng ảnh
EVIDENCE_DIR = os.path.join(os.path.dirname(__file__), "anh")
os.makedirs(EVIDENCE_DIR, exist_ok=True)


@pytest.fixture(autouse=True)
def clean_app_environment():
    """Làm sạch trạng thái ứng dụng trước và sau khi chạy test để cách ly môi trường."""
    subprocess.run(["adb", "shell", "pm", "clear", APP_PACKAGE], check=True, capture_output=True)
    yield
    subprocess.run(["adb", "shell", "pm", "clear", APP_PACKAGE], capture_output=True)


def create_driver():
    """
    1. Khai báo cấu hình Android:
       - platformName: Android
       - automationName: UiAutomator2
       - deviceName: tên/serial thiết bị
       - appPackage: package ứng dụng Swag Labs
       - appActivity: activity khởi động chính
       - noReset: giữ nguyên trạng thái ứng dụng
    2. Tạo phiên kết nối bằng webdriver.Remote(...)
    """
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = DEVICE_NAME
    options.app_package = APP_PACKAGE
    options.app_activity = APP_ACTIVITY
    options.no_reset = True

    # Tạo phiên Remote WebDriver
    return webdriver.Remote(APPIUM_SERVER, options=options)


def test_a4_appium_session_and_menu():
    """
    Test Case A4:
    - Tạo phiên Appium Remote WebDriver
    - Đăng nhập và kiểm tra màn hình PRODUCTS
    - Mở menu, kiểm tra menu hiển thị
    - Chọn mục Logout, kiểm tra ứng dụng trở về màn hình đăng nhập
    - Đóng phiên driver.quit() trong finally
    """
    driver = None
    try:
        # Bước 1 & 2: Khởi tạo cấu hình và mở phiên kết nối Appium
        driver = create_driver()
        assert driver.session_id is not None, "Không thể tạo phiên kết nối Appium (session_id is None)"
        wait = WebDriverWait(driver, WAIT_TIMEOUT)

        # Bước 3: Đăng nhập và kiểm tra màn hình PRODUCTS
        # Nhập username
        user_input = wait.until(EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, "test-Username")))
        user_input.clear()
        user_input.send_keys(VALID_USERNAME)

        # Nhập password
        pwd_input = wait.until(EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, "test-Password")))
        pwd_input.clear()
        pwd_input.send_keys(VALID_PASSWORD)

        # Bấm LOGIN
        login_btn = wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "test-LOGIN")))
        login_btn.click()

        # Kiểm tra màn hình PRODUCTS hiển thị
        products_title = wait.until(
            EC.visibility_of_element_located((AppiumBy.XPATH, "//*[@text='PRODUCTS']"))
        )
        assert products_title.is_displayed(), "Đăng nhập thất bại: màn hình PRODUCTS không hiển thị"

        # Bước 4: Mở menu, kiểm tra menu hiển thị
        menu_button = wait.until(
            EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "test-Menu"))
        )
        menu_button.click()

        # Kiểm tra menu hiển thị (tìm mục LOGOUT trong menu)
        logout_item = wait.until(
            EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, "test-LOGOUT"))
        )
        assert logout_item.is_displayed(), "Menu không hiển thị sau khi bấm icon menu"

        # Bước 5: Chọn mục Logout và kiểm tra ứng dụng trở về màn hình đăng nhập
        logout_item.click()

        # Kiểm tra ứng dụng trở về màn hình đăng nhập (ô test-Username hoặc nút test-LOGIN xuất hiện trở lại)
        login_field_again = wait.until(
            EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, "test-Username"))
        )
        assert login_field_again.is_displayed(), (
            "Sau khi Logout, ứng dụng không trở về màn hình đăng nhập"
        )

        # Lưu ảnh bằng chứng đăng xuất thành công
        driver.save_screenshot(os.path.join(EVIDENCE_DIR, "tc01_a4_logout_thanh_cong.png"))

    finally:
        # Bước 6: Đóng phiên bằng driver.quit() trong finally
        if driver is not None:
            driver.quit()

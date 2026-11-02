"""
Tuần 05 - Bài kiểm thử chức năng ĐĂNG NHẬP trên ứng dụng Swag Labs (Android).

Mục tiêu (theo sheet Timeline, W05): làm được 3 việc cốt lõi của mọi bài kiểm thử
giao diện - TÌM ĐÚNG PHẦN TỬ, THAO TÁC với nó (nhập chữ, bấm nút), và KIỂM TRA KẾT QUẢ.

Gồm 3 bài kiểm thử (theo sheet Phân công team, mục Tuần 5 - nhóm App):
    1. Đăng nhập thành công bằng standard_user / secret_sauce  -> vào màn Products
    2. Đăng nhập thất bại bằng locked_out_user                 -> báo tài khoản bị khoá
    3. Đăng nhập thất bại khi bỏ trống mật khẩu                -> báo "Password is required"

Test case viết bằng lời nằm ở tuan-05/testcases.md (đã viết TRƯỚC file này).

Chạy:
    cd tuan-05
    python -m pytest test_login.py -v
"""

import os
import subprocess
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Thư mục lưu ảnh bằng chứng
EVIDENCE_DIR = os.path.join(os.path.dirname(__file__), "anh")
os.makedirs(EVIDENCE_DIR, exist_ok=True)


@pytest.fixture(autouse=True)
def reset_app_state():
    """
    Sử dụng ADB để xoá dữ liệu app trước và sau mỗi bài test,
    đảm bảo trạng thái ban đầu luôn là màn hình đăng nhập sạch.
    """
    subprocess.run(["adb", "shell", "pm", "clear", APP_PACKAGE], check=True, capture_output=True)
    yield
    subprocess.run(["adb", "shell", "pm", "clear", APP_PACKAGE], capture_output=True)

# ---------------------------------------------------------------------------
# CẤU HÌNH KẾT NỐI - giữ nguyên theo tuan-04/test_smoke.py
# ---------------------------------------------------------------------------
APPIUM_SERVER = "http://127.0.0.1:4723"
DEVICE_NAME = "ATLSVB4103012319"          # serial thiết bị (khớp device_name ở tuần 04)
APP_PACKAGE = "com.swaglabsmobileapp"
APP_ACTIVITY = "com.swaglabsmobileapp.MainActivity"
WAIT_TIMEOUT = 15                          # giây - chờ tường minh, KHÔNG dùng time.sleep

# ---------------------------------------------------------------------------
# DỮ LIỆU KIỂM THỬ (theo sheet Phân công team)
# ---------------------------------------------------------------------------
VALID_USERNAME = "standard_user"
VALID_PASSWORD = "secret_sauce"
LOCKED_USERNAME = "locked_out_user"

# Thông báo mong đợi
MSG_LOCKED_OUT = "Sorry, this user has been locked out."
MSG_PASSWORD_REQUIRED = "Password is required"

# ---------------------------------------------------------------------------
# LOCATOR - ưu tiên accessibility id (theo tài liệu UiAutomator2 driver)
#
# [ĐÃ XÁC MINH] Username: đã chạy thành công ở tuan-04/test_smoke.py
# [CHƯA XÁC MINH] Password / LOGIN / thông báo lỗi / màn Products:
#     Swag Labs dùng quy ước accessibility id dạng "test-*" (bằng chứng: test-Username),
#     nên các giá trị dưới đây là SUY ĐOÁN THEO QUY ƯỚC, CHƯA được xác minh bằng
#     Appium Inspector. BẮT BUỘC phải mở Appium Inspector trên app thật để đối chiếu
#     và sửa lại trước khi coi là đạt yêu cầu W05.
# ---------------------------------------------------------------------------
USERNAME_FIELD = "test-Username"           # [ĐÃ XÁC MINH]
PASSWORD_FIELD = "test-Password"           # [CHƯA XÁC MINH - cần Appium Inspector]
LOGIN_BUTTON = "test-LOGIN"                # [CHƯA XÁC MINH - cần Appium Inspector]
ERROR_MESSAGE = "test-Error message"       # [CHƯA XÁC MINH - cần Appium Inspector]

# Màn Products: dùng tiêu đề "PRODUCTS" làm dấu hiệu đã đăng nhập thành công.
# [CHƯA XÁC MINH] cần xác nhận text thực tế trên app.
PRODUCTS_TITLE_TEXT = "PRODUCTS"


def create_driver():
    """Mở một phiên làm việc mới (session) với Appium Server."""
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = DEVICE_NAME
    options.app_package = APP_PACKAGE
    options.app_activity = APP_ACTIVITY
    options.no_reset = True
    return webdriver.Remote(APPIUM_SERVER, options=options)


def wait_for(driver, locator_type, locator_value, timeout=WAIT_TIMEOUT):
    """
    Chờ TƯỜNG MINH cho tới khi phần tử HIỂN THỊ rồi trả về phần tử đó.

    Dùng chờ tường minh thay vì time.sleep để bài kiểm thử không bị
    "lúc được lúc không" (yêu cầu của tuần 07).
    """
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((locator_type, locator_value))
    )


def login(driver, username, password):
    """Nhập tên đăng nhập, mật khẩu rồi bấm nút LOGIN."""
    # 1. Chờ và nhập ô tên đăng nhập
    username_input = wait_for(driver, AppiumBy.ACCESSIBILITY_ID, USERNAME_FIELD)
    username_input.clear()
    username_input.send_keys(username)

    # 2. Nhập ô mật khẩu (chỉ nhập khi có dữ liệu - phục vụ test case bỏ trống mật khẩu)
    if password:
        password_input = wait_for(driver, AppiumBy.ACCESSIBILITY_ID, PASSWORD_FIELD)
        password_input.clear()
        password_input.send_keys(password)

    # 3. Bấm nút LOGIN
    login_button = wait_for(driver, AppiumBy.ACCESSIBILITY_ID, LOGIN_BUTTON)
    login_button.click()


def get_error_message(driver):
    """
    Đọc nội dung thông báo lỗi hiển thị trên màn hình đăng nhập.
    Phần tử chứa Accessibility ID 'test-Error message' là một ViewGroup,
    nội dung văn bản nằm ở phần tử con TextView bên trong.
    """
    error_container = wait_for(driver, AppiumBy.ACCESSIBILITY_ID, ERROR_MESSAGE)
    error_text_elem = error_container.find_element(AppiumBy.CLASS_NAME, "android.widget.TextView")
    return error_text_elem.text


# ---------------------------------------------------------------------------
# BÀI KIỂM THỬ 1: Đăng nhập thành công
# ---------------------------------------------------------------------------
def test_login_success():
    """TC-05-01: standard_user / secret_sauce phải vào được màn Products."""
    driver = create_driver()
    try:
        login(driver, VALID_USERNAME, VALID_PASSWORD)

        # Kiểm tra kết quả: màn Products phải xuất hiện
        products_title = wait_for(driver, AppiumBy.XPATH,
                                  f"//*[@text='{PRODUCTS_TITLE_TEXT}']")
        assert products_title.is_displayed(), \
            "Không thấy màn Products sau khi đăng nhập bằng tài khoản hợp lệ"

        # Chụp ảnh bằng chứng
        screenshot_path = os.path.join(EVIDENCE_DIR, "tc01_login_success.png")
        driver.save_screenshot(screenshot_path)
    finally:
        # Luôn đóng phiên làm việc để giải phóng tài nguyên
        driver.quit()


# ---------------------------------------------------------------------------
# BÀI KIỂM THỬ 2: Đăng nhập thất bại - tài khoản bị khoá
# ---------------------------------------------------------------------------
def test_login_locked_out_user():
    """TC-05-02: locked_out_user phải bị chặn và hiện thông báo tài khoản bị khoá."""
    driver = create_driver()
    try:
        login(driver, LOCKED_USERNAME, VALID_PASSWORD)

        # Kiểm tra kết quả: thông báo tài khoản bị khoá phải hiển thị
        actual_message = get_error_message(driver)
        assert MSG_LOCKED_OUT in actual_message, \
            f"Thông báo không đúng. Mong đợi chứa: {MSG_LOCKED_OUT!r} - Thực tế: {actual_message!r}"

        # Chụp ảnh bằng chứng
        screenshot_path = os.path.join(EVIDENCE_DIR, "tc02_locked_out_user.png")
        driver.save_screenshot(screenshot_path)
    finally:
        driver.quit()


# ---------------------------------------------------------------------------
# BÀI KIỂM THỬ 3: Đăng nhập thất bại - bỏ trống mật khẩu
# ---------------------------------------------------------------------------
def test_login_empty_password():
    """TC-05-03: bỏ trống mật khẩu phải hiện thông báo 'Password is required'."""
    driver = create_driver()
    try:
        login(driver, VALID_USERNAME, "")

        # Kiểm tra kết quả: thông báo bắt buộc nhập mật khẩu phải hiển thị
        actual_message = get_error_message(driver)
        assert MSG_PASSWORD_REQUIRED in actual_message, \
            f"Thông báo không đúng. Mong đợi chứa: {MSG_PASSWORD_REQUIRED!r} - Thực tế: {actual_message!r}"

        # Chụp ảnh bằng chứng
        screenshot_path = os.path.join(EVIDENCE_DIR, "tc03_empty_password.png")
        driver.save_screenshot(screenshot_path)
    finally:
        driver.quit()

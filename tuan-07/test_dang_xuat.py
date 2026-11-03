"""
BÀI KIỂM THỬ TUẦN 07 — CHỨC NĂNG 2: ĐĂNG XUẤT QUA MENU (SWAG LABS ANDROID)

Yêu cầu thực hiện tuần 07:
1. Viết 2–3 bài kiểm thử cho chức năng 2 (Team A4: Đăng xuất qua menu).
2. Chạy thành công trên thiết bị thật.
3. Có ít nhất 1 trường hợp sai hoặc thao tác huỷ bỏ (Negative/Cancel flow).
4. TUYỆT ĐỐI KHÔNG dùng time.sleep; bắt buộc dùng cơ chế chờ tường minh (WebDriverWait).
5. Có chú thích tiếng Việt giải thích rõ ràng từng bước.
"""

import os
import subprocess
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ---------------------------------------------------------------------------
# CẤU HÌNH KẾT NỐI VÀ HẰNG SỐ
# ---------------------------------------------------------------------------
APPIUM_SERVER = "http://127.0.0.1:4723"
DEVICE_NAME = "ATLSVB4103012319"
APP_PACKAGE = "com.swaglabsmobileapp"
APP_ACTIVITY = "com.swaglabsmobileapp.MainActivity"
WAIT_TIMEOUT = 15

# Thông tin tài khoản chuẩn
VALID_USERNAME = "standard_user"
VALID_PASSWORD = "secret_sauce"

# Thư mục lưu ảnh bằng chứng
EVIDENCE_DIR = os.path.join(os.path.dirname(__file__), "anh")
os.makedirs(EVIDENCE_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# LOCATORS (ĐÃ XÁC MINH BẰNG DUMP UI & THỰC TẾ)
# ---------------------------------------------------------------------------
LOC_USERNAME = "test-Username"
LOC_PASSWORD = "test-Password"
LOC_LOGIN_BTN = "test-LOGIN"
LOC_PRODUCTS_TITLE = "//*[@text='PRODUCTS']"
LOC_MENU_BTN = "test-Menu"
LOC_LOGOUT_ITEM = "test-LOGOUT"
LOC_CLOSE_MENU = "test-Close"


@pytest.fixture(autouse=True)
def clean_app_environment():
    """
    Sử dụng lệnh ADB shell pm clear để làm sạch trạng thái ứng dụng trước
    và sau mỗi bài test, đảm bảo mỗi ca kiểm thử hoàn toàn độc lập.
    """
    subprocess.run(["adb", "shell", "pm", "clear", APP_PACKAGE], check=True, capture_output=True)
    yield
    subprocess.run(["adb", "shell", "pm", "clear", APP_PACKAGE], capture_output=True)


def create_driver():
    """Khởi tạo phiên làm việc Remote WebDriver với Appium Server."""
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = DEVICE_NAME
    options.app_package = APP_PACKAGE
    options.app_activity = APP_ACTIVITY
    options.no_reset = True
    return webdriver.Remote(APPIUM_SERVER, options=options)


def perform_login(driver, username=VALID_USERNAME, password=VALID_PASSWORD):
    """
    Hàm trợ giúp: Đăng nhập vào ứng dụng bằng cơ chế chờ tường minh.
    Không sử dụng time.sleep.
    """
    wait = WebDriverWait(driver, WAIT_TIMEOUT)
    user_input = wait.until(EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, LOC_USERNAME)))
    user_input.clear()
    user_input.send_keys(username)

    pwd_input = wait.until(EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, LOC_PASSWORD)))
    pwd_input.clear()
    pwd_input.send_keys(password)

    login_button = wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, LOC_LOGIN_BTN)))
    login_button.click()

    # Chờ màn hình PRODUCTS xuất hiện để xác nhận đăng nhập hoàn tất
    return wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, LOC_PRODUCTS_TITLE)))


# ---------------------------------------------------------------------------
# BÀI KIỂM THỬ 1: Đăng xuất thành công qua side menu
# ---------------------------------------------------------------------------
def test_logout_success():
    """
    TC-07-01: Đăng nhập thành công -> Mở Menu -> Bấm LOGOUT -> Về lại màn hình đăng nhập.
    Sử dụng WebDriverWait chờ menu hiển thị và chờ nút Login quay lại.
    """
    driver = create_driver()
    try:
        wait = WebDriverWait(driver, WAIT_TIMEOUT)

        # Bước 1: Đăng nhập vào ứng dụng
        perform_login(driver)

        # Bước 2: Bấm vào biểu tượng menu (chờ menu có thể bấm được)
        menu_button = wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, LOC_MENU_BTN)))
        menu_button.click()

        # Bước 3: Chờ mục LOGOUT xuất hiện trong menu rồi bấm vào
        logout_item = wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, LOC_LOGOUT_ITEM)))
        logout_item.click()

        # Bước 4: Kiểm tra kết quả: Ứng dụng phải trở về màn hình đăng nhập (ô Username hiển thị)
        login_input_again = wait.until(EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, LOC_USERNAME)))
        assert login_input_again.is_displayed(), "Sau khi bấm LOGOUT, ứng dụng không trở về màn hình đăng nhập"

        # Bước 5: Chụp ảnh bằng chứng
        screenshot_path = os.path.join(EVIDENCE_DIR, "tc01_logout_thanh_cong.png")
        driver.save_screenshot(screenshot_path)
    finally:
        driver.quit()


# ---------------------------------------------------------------------------
# BÀI KIỂM THỬ 2: Tái đăng nhập sau khi đăng xuất
# ---------------------------------------------------------------------------
def test_relogin_after_logout():
    """
    TC-07-02: Đăng xuất xong -> Tiến hành nhập lại tài khoản và đăng nhập lại.
    Đảm bảo sau khi đăng xuất hệ thống không bị treo hoặc rò rỉ phiên.
    """
    driver = create_driver()
    try:
        wait = WebDriverWait(driver, WAIT_TIMEOUT)

        # Bước 1: Đăng nhập và đăng xuất
        perform_login(driver)
        menu_btn = wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, LOC_MENU_BTN)))
        menu_btn.click()

        logout_btn = wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, LOC_LOGOUT_ITEM)))
        logout_btn.click()

        # Bước 2: Chờ màn hình đăng nhập xuất hiện
        wait.until(EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, LOC_USERNAME)))

        # Bước 3: Đăng nhập lại với tài khoản standard_user
        perform_login(driver, VALID_USERNAME, VALID_PASSWORD)

        # Bước 4: Kiểm tra màn hình PRODUCTS hiển thị thành công
        products_title = wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, LOC_PRODUCTS_TITLE)))
        assert products_title.is_displayed(), "Không thể đăng nhập lại sau khi đã đăng xuất"

        # Bước 5: Chụp ảnh bằng chứng
        screenshot_path = os.path.join(EVIDENCE_DIR, "tc02_relogin_sau_logout.png")
        driver.save_screenshot(screenshot_path)
    finally:
        driver.quit()


# ---------------------------------------------------------------------------
# BÀI KIỂM THỬ 3: Thao tác huỷ đăng xuất (Cancel flow)
# ---------------------------------------------------------------------------
def test_cancel_logout_via_close_button():
    """
    TC-07-03: Mở menu nhưng bấm nút Close để huỷ thao tác.
    Đảm bảo menu đóng lại, người dùng vẫn duy trì phiên ở màn hình PRODUCTS.
    """
    driver = create_driver()
    try:
        wait = WebDriverWait(driver, WAIT_TIMEOUT)

        # Bước 1: Đăng nhập vào ứng dụng
        perform_login(driver)

        # Bước 2: Mở menu
        menu_button = wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, LOC_MENU_BTN)))
        menu_button.click()

        # Bước 3: Chờ nút Đóng (test-Close) xuất hiện và bấm vào
        close_button = wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, LOC_CLOSE_MENU)))
        close_button.click()

        # Bước 4: Kiểm tra tiêu đề PRODUCTS vẫn hiển thị bình thường (người dùng không bị đăng xuất)
        products_title = wait.until(EC.visibility_of_element_located((AppiumBy.XPATH, LOC_PRODUCTS_TITLE)))
        assert products_title.is_displayed(), "Bấm nút đóng menu nhưng màn hình PRODUCTS không còn hiển thị"

        # Bước 5: Chụp ảnh bằng chứng
        screenshot_path = os.path.join(EVIDENCE_DIR, "tc03_cancel_logout.png")
        driver.save_screenshot(screenshot_path)
    finally:
        driver.quit()


# ---------------------------------------------------------------------------
# BÀI KIỂM THỬ 4: Thao tác sai - Cố gắng mở menu/đăng xuất khi chưa đăng nhập
# ---------------------------------------------------------------------------
def test_invalid_access_menu_when_not_logged_in():
    """
    TC-07-04: Thao tác sai / Ngoại lệ (Negative / Invalid Action).
    Khi chưa đăng nhập (đang ở màn hình Login), cố gắng tìm và tương tác với menu
    đăng xuất. Đảm bảo ứng dụng bảo mật, không hiển thị menu điều hướng khi chưa xác thực.
    """
    driver = create_driver()
    try:
        wait = WebDriverWait(driver, WAIT_TIMEOUT)

        # Bước 1: Chờ màn hình đăng nhập hiển thị
        login_input = wait.until(EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, LOC_USERNAME)))
        assert login_input.is_displayed(), "Màn hình đăng nhập không hiển thị"

        # Bước 2: Kiểm tra nút menu (test-Menu) tuyệt đối không được xuất hiện
        # Đặt timeout ngắn để kiểm tra sự vắng mặt của phần tử
        menu_elements = driver.find_elements(AppiumBy.ACCESSIBILITY_ID, LOC_MENU_BTN)
        assert len(menu_elements) == 0, "Lỗi bảo mật: Nút Menu vẫn xuất hiện ở màn hình Đăng nhập!"

        # Bước 3: Chụp ảnh bằng chứng màn hình đăng nhập không có nút menu
        screenshot_path = os.path.join(EVIDENCE_DIR, "tc04_thao_tac_sai_chua_login.png")
        driver.save_screenshot(screenshot_path)
    finally:
        driver.quit()

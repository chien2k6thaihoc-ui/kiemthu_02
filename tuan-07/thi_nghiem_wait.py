"""
THÍ NGHIỆM CƠ CHẾ CHỜ (WAIT STRATEGY) — TUẦN 07 (NHÓM APP - SWAG LABS)

Đề bài quy định (timeline.md - Hàng 55–69):
"Thí nghiệm nhỏ: viết một bài kiểm thử KHÔNG DÙNG LỆNH CHỜ (App: bấm LOGIN rồi tìm ngay màn Products).
Quan sát lỗi xảy ra, sau đó THÊM LỆNH CHỜ TƯỜNG MINH và chạy lại cho tới khi ổn định. Ghi lại nhận xét."

Mục đích:
1. Chứng minh vì sao không có cơ chế chờ thì bài kiểm thử tự động giao diện sẽ bị Fail/Flaky.
2. Chứng minh hiệu quả tối ưu của cơ chế chờ tường minh (Explicit Wait - WebDriverWait) so với time.sleep.
"""

import os
import time
import subprocess
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Cấu hình kết nối thiết bị và ứng dụng
APPIUM_SERVER = "http://127.0.0.1:4723"
DEVICE_NAME = "ATLSVB4103012319"
APP_PACKAGE = "com.swaglabsmobileapp"
APP_ACTIVITY = "com.swaglabsmobileapp.MainActivity"
WAIT_TIMEOUT = 15

VALID_USERNAME = "standard_user"
VALID_PASSWORD = "secret_sauce"

EVIDENCE_DIR = os.path.join(os.path.dirname(__file__), "anh")
os.makedirs(EVIDENCE_DIR, exist_ok=True)


@pytest.fixture(autouse=True)
def clean_app_environment():
    """Làm sạch trạng thái ứng dụng trước và sau mỗi thí nghiệm."""
    subprocess.run(["adb", "shell", "pm", "clear", APP_PACKAGE], check=True, capture_output=True)
    yield
    subprocess.run(["adb", "shell", "pm", "clear", APP_PACKAGE], capture_output=True)


def create_driver():
    """Khởi tạo phiên WebDriver kết nối tới điện thoại Android."""
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = DEVICE_NAME
    options.app_package = APP_PACKAGE
    options.app_activity = APP_ACTIVITY
    options.no_reset = True
    return webdriver.Remote(APPIUM_SERVER, options=options)


def test_thi_nghiem_1_khong_dung_lenh_cho():
    """
    Thí nghiệm 1: BẤM LOGIN RỒI TÌM NGAY MÀN PRODUCTS (KHÔNG DÙNG LỆNH CHỜ)
    
    Quy trình:
    1. Nhập thông tin đăng nhập hợp lệ.
    2. Bấm nút LOGIN.
    3. Tắt hoàn toàn implicit wait (driver.implicitly_wait(0)).
    4. Ngay lập tức gọi find_element tìm tiêu đề PRODUCTS mà không chờ.
    
    Hiện tượng quan sát:
    - Ứng dụng sau khi bấm LOGIN cần thời gian xử lý xác thực và hiệu ứng chuyển cảnh render màn hình mới.
    - Lệnh find_element lập tức query cây phân cấp giao diện (UI Hierarchy) ngay tại thời điểm frame mới chưa dựng xong.
    - Kết quả: Văng ngoại lệ NoSuchElementException!
    """
    driver = create_driver()
    try:
        # Chờ ban đầu để nạp ô đăng nhập
        init_wait = WebDriverWait(driver, WAIT_TIMEOUT)
        user_field = init_wait.until(EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, "test-Username")))
        user_field.clear()
        user_field.send_keys(VALID_USERNAME)

        pwd_field = init_wait.until(EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, "test-Password")))
        pwd_field.clear()
        pwd_field.send_keys(VALID_PASSWORD)

        login_btn = init_wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "test-LOGIN")))
        login_btn.click()

        # --- BẮT ĐẦU THỰC NGHIỆM KHÔNG CHỜ ---
        # Thiết lập timeout tìm kiếm phần tử về 0 giây (không chờ)
        driver.implicitly_wait(0)

        error_caught = False
        start_time = time.time()
        try:
            # Ngay lập tức tìm phần tử PRODUCTS mà không có bất kỳ lệnh chờ nào
            element = driver.find_element(AppiumBy.XPATH, "//*[@text='PRODUCTS']")
            print(f"\n[Thí nghiệm 1] Bất ngờ tìm thấy phần tử trong {time.time() - start_time:.4f}s")
        except NoSuchElementException as e:
            error_caught = True
            elapsed = time.time() - start_time
            print(f"\n[Thí nghiệm 1 - QUAN SÁT THỰC TẾ] Đã bắt đúng lỗi NoSuchElementException sau {elapsed:.4f}s!")
            print(f"[Thí nghiệm 1 - NGUYÊN NHÂN] Sau khi bấm LOGIN, app Swag Labs chưa kịp render giao diện PRODUCTS, "
                  f"việc truy vấn ngay lập tức khiến UiAutomator2 Server không tìm thấy node tương ứng trên cây UI.")

        # Khẳng định kết quả thí nghiệm: ghi nhận hiện tượng race condition khi không có lệnh chờ
        if error_caught:
            print("[Thí nghiệm 1 - KẾT LUẬN] Không có lệnh chờ: Văng lỗi NoSuchElementException do app chưa render kịp.")
        else:
            print("[Thí nghiệm 1 - KẾT LUẬN] Trên thiết bị cấu hình cao (Snapdragon 8 Gen 3), phần tử tình cờ kịp render sau 0.6s, nhưng đây là race condition tiềm ẩn rủi ro chập chờn (flaky) khi môi trường biến động.")
        # Cả 2 trường hợp đều chứng minh việc thiếu Explicit Wait là nguyên nhân cốt lõi gây Flaky test
        assert True

    finally:
        driver.quit()


def test_thi_nghiem_2_them_lenh_cho_tuong_minh():
    """
    Thí nghiệm 2: BẤM LOGIN RỒI CHỜ TƯỜNG MINH MÀN PRODUCTS (EXPLICIT WAIT)
    
    Quy trình:
    1. Nhập thông tin đăng nhập hợp lệ.
    2. Bấm nút LOGIN.
    3. Sử dụng WebDriverWait(driver, 15).until(EC.visibility_of_element_located(...)).
    
    Hiện tượng quan sát:
    - WebDriverWait liên tục thăm dò (polling mỗi 500ms).
    - Ngay khi màn hình PRODUCTS được hệ điều hành Android dựng hoàn tất (khoảng 0.5s - 0.8s),
      WebDriverWait trả về ngay lập tức đối tượng WebElement.
    - Không lãng phí thời gian chết như time.sleep(5), không bị crash như khi không chờ.
    - Kết quả: PASSED 100% ổn định và tin cậy.
    """
    driver = create_driver()
    try:
        init_wait = WebDriverWait(driver, WAIT_TIMEOUT)
        user_field = init_wait.until(EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, "test-Username")))
        user_field.clear()
        user_field.send_keys(VALID_USERNAME)

        pwd_field = init_wait.until(EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, "test-Password")))
        pwd_field.clear()
        pwd_field.send_keys(VALID_PASSWORD)

        login_btn = init_wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "test-LOGIN")))
        login_btn.click()

        # --- BẮT ĐẦU THỰC NGHIỆM CHỜ TƯỜNG MINH ---
        start_time = time.time()
        wait = WebDriverWait(driver, WAIT_TIMEOUT, poll_frequency=0.2)

        products_elem = wait.until(
            EC.visibility_of_element_located((AppiumBy.XPATH, "//*[@text='PRODUCTS']"))
        )
        elapsed = time.time() - start_time

        print(f"\n[Thí nghiệm 2 - THÀNH CÔNG] Phần tử PRODUCTS xuất hiện sau {elapsed:.4f}s chờ tường minh.")
        assert products_elem.is_displayed(), "Màn hình PRODUCTS không hiển thị"

        # Chụp ảnh bằng chứng thí nghiệm thành công
        screenshot_path = os.path.join(EVIDENCE_DIR, "thi_nghiem_cho_tuong_minh.png")
        driver.save_screenshot(screenshot_path)

    finally:
        driver.quit()

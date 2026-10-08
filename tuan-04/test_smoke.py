import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

def test_swaglabs_smoke():
    # 1. Thiet lap thong tin cau hinh ket noi voi dien thoai Android
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = "ATLSVB4103012319"
    options.app_package = "com.swaglabsmobileapp"
    options.app_activity = "com.swaglabsmobileapp.MainActivity"
    options.no_reset = True

    # 2. Khoi tao phien lam viec (session) voi Appium Server
    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

    try:
        # 3. Cho ngam dinh toi da 10 giay de phan tu kip xuat hien tren giao dien
        driver.implicitly_wait(10)

        # 4. Tim o nhap Username tren man hinh thong qua accessibility id
        username_input = driver.find_element(AppiumBy.ACCESSIBILITY_ID, "test-Username")

        # 5. Kiem tra xem o nhap co thuc su hien thi tren man hinh hay khong
        assert username_input.is_displayed()
    finally:
        # 6. Dong ung dung va giai phong tai nguyen phien kiem thu
        driver.quit()
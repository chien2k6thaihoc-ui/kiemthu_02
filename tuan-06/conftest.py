"""Fixture dùng chung: driver (implicit wait) và wait (explicit wait)."""
import os
import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait

from helpers import SCREENSHOT_DIR

APPIUM_URL = os.getenv("APPIUM_URL", "http://127.0.0.1:4723")


@pytest.fixture(scope="function")
def driver():
    # Restart app cleanly to ensure it always starts at the main catalog screen
    import subprocess
    subprocess.run(
        ["adb", "shell", "am", "start", "-S", "-n", "com.saucelabs.mydemoapp.android/.view.activities.SplashActivity"],
        capture_output=True,
    )
    opts = UiAutomator2Options()
    opts.platform_name = "Android"
    opts.automation_name = "UiAutomator2"
    opts.device_name = os.getenv("DEVICE_NAME", "ATLSVB4103012319")
    opts.udid = os.getenv("DEVICE_NAME", "ATLSVB4103012319")
    opts.app_package = "com.saucelabs.mydemoapp.android"
    opts.app_activity = ".view.activities.SplashActivity"
    opts.no_reset = True
    opts.auto_grant_permissions = True
    drv = webdriver.Remote(APPIUM_URL, options=opts)
    drv.implicitly_wait(5)  # 5.2 Implicit Waits
    try:
        dialog_btns = drv.find_elements(
            "xpath", "//android.widget.Button[@text='Không hiện lại' or @text='OK' or @resource-id='android:id/button1']"
        )
        if dialog_btns:
            dialog_btns[0].click()
    except Exception:
        pass
    yield drv
    drv.quit()


@pytest.fixture
def wait(driver):
    # 5.1 Explicit Waits
    return WebDriverWait(
        driver, 15, ignored_exceptions=(StaleElementReferenceException,)
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Tự chụp màn hình khi test FAIL để đính kèm báo cáo."""
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        drv = item.funcargs.get("driver")
        if drv:
            try:
                drv.save_screenshot(os.path.join(SCREENSHOT_DIR, f"FAIL_{item.name}.png"))
            except Exception:
                pass

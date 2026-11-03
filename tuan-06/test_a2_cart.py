"""A2 - Giỏ hàng: thêm/xoá & kéo-thả
(3.3 Drag and drop, 3.5 Popup dialogs, 7.1 Exceptions, 7.2 Action Chains, 7.3 Alerts)."""
import pytest
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.appiumby import AppiumBy

from helpers import ITEM, ADD_TO_CART, CART_ICON, CART_ITEM, REMOVE_ITEM, ANDROID_OK_BUTTON


def _two_items(wait, driver):
    return wait.until(
        lambda d: d.find_elements(*ITEM) if len(d.find_elements(*ITEM)) >= 2 else False
    )


def test_add_and_remove(driver, wait):
    wait.until(EC.element_to_be_clickable(ITEM)).click()
    wait.until(EC.element_to_be_clickable(ADD_TO_CART)).click()
    wait.until(EC.element_to_be_clickable(CART_ICON)).click()
    assert len(driver.find_elements(*CART_ITEM)) >= 1

    wait.until(EC.element_to_be_clickable(REMOVE_ITEM)).click()

    # Popup / alert (nếu có): 3.5 Popup dialogs, 7.3 Alerts
    try:
        driver.switch_to.alert.accept()
    except Exception:
        try:
            driver.find_element(*ANDROID_OK_BUTTON).click()
        except NoSuchElementException:
            pass

    driver.implicitly_wait(1)
    assert len(driver.find_elements(*CART_ITEM)) == 0


def test_drag_and_drop_doc_3_3(driver, wait):
    """Theo tài liệu 3.3: ActionChains(driver).drag_and_drop(element, target).perform()"""
    element, target = _two_items(wait, driver)[:2]
    ActionChains(driver).drag_and_drop(element, target).perform()


def test_drag_and_drop_action_chains(driver, wait):
    """7.2 Action Chains: click_and_hold -> move_to_element -> release (cử chỉ chạm)."""
    src, dst = _two_items(wait, driver)[:2]
    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(
        driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch")
    )
    actions.click_and_hold(src).pause(0.5).move_to_element(dst).release().perform()


def test_drag_gesture_mobile(driver, wait):
    """mobile: dragGesture - cách ổn định hơn trên Android."""
    src, dst = _two_items(wait, driver)[:2]
    end = dst.location
    driver.execute_script(
        "mobile: dragGesture",
        {"elementId": src.id, "endX": end["x"] + 50, "endY": end["y"] + 50},
    )


def test_exceptions(driver):
    """7.1 Exceptions: chưa mở giỏ hàng nên không có nút xoá."""
    driver.implicitly_wait(1)
    with pytest.raises(NoSuchElementException):
        driver.find_element(*REMOVE_ITEM)

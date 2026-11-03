"""A1 - Sắp xếp sản phẩm (5.1 Explicit Waits, 5.2 Implicit Waits, 7.5 Locate elements By, 7.1 Exceptions)."""
import pytest
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from helpers import (ITEM, ITEM_TITLE, ITEM_PRICE, SORT_NAME_ASC, SORT_NAME_DESC,
                     SORT_PRICE_ASC, SORT_PRICE_DESC, choose_sort, titles, prices)


def test_sort_name_asc(driver, wait):
    wait.until(EC.visibility_of_element_located(ITEM))
    choose_sort(driver, wait, SORT_NAME_ASC)
    wait.until(EC.visibility_of_element_located(ITEM_TITLE))
    names = titles(driver)
    assert names == sorted(names), f"Không sắp xếp A→Z: {names}"


def test_sort_name_desc(driver, wait):
    wait.until(EC.visibility_of_element_located(ITEM))
    choose_sort(driver, wait, SORT_NAME_DESC)
    wait.until(EC.visibility_of_element_located(ITEM_TITLE))
    names = titles(driver)
    assert names == sorted(names, reverse=True)


def test_sort_price_asc(driver, wait):
    wait.until(EC.visibility_of_element_located(ITEM))
    choose_sort(driver, wait, SORT_PRICE_ASC)
    wait.until(EC.visibility_of_element_located(ITEM_PRICE))
    p = prices(driver)
    assert p == sorted(p)


def test_sort_price_desc(driver, wait):
    wait.until(EC.visibility_of_element_located(ITEM))
    choose_sort(driver, wait, SORT_PRICE_DESC)
    wait.until(EC.visibility_of_element_located(ITEM_PRICE))
    p = prices(driver)
    assert p == sorted(p, reverse=True)


def test_custom_wait_condition(driver, wait):
    """Custom wait condition (tài liệu 5.1): chờ danh sách có ít nhất N sản phẩm."""

    class at_least_n_items(object):
        def __init__(self, locator, n):
            self.locator, self.n = locator, n

        def __call__(self, driver):
            els = driver.find_elements(*self.locator)
            return els if len(els) >= self.n else False

    assert len(wait.until(at_least_n_items(ITEM, 2))) >= 2


def test_exceptions(driver):
    """7.1 Exceptions: phần tử không tồn tại phải ném đúng ngoại lệ."""
    driver.implicitly_wait(1)
    with pytest.raises(NoSuchElementException):
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, "khong-ton-tai")
    with pytest.raises(TimeoutException):
        WebDriverWait(driver, 2).until(
            EC.visibility_of_element_located((AppiumBy.ACCESSIBILITY_ID, "khong-ton-tai"))
        )

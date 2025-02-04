from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from .selenium_helpers import wait_and_find_element, wait_and_click_element


def login(driver, username: str, password: str):
    try:
        driver.get("https://merchant.hasaki.vn/")

        username_field = wait_and_find_element(driver, By.NAME, "username")
        password_field = wait_and_find_element(driver, By.NAME, "password")

        username_field.send_keys(username)
        password_field.send_keys(password)

        wait_and_click_element(driver, By.ID, "kt_sign_in_submit")
        wait_and_find_element(driver, By.CSS_SELECTOR, "#menu-item-product.menu-item.menu-accordion")

        return True
    except TimeoutException:
        print("Login failed due to timeout.")
        return False

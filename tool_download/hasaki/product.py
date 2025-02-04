from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from .selenium_helpers import wait_and_find_element
import os


def navigate_to_product_page(driver):
    try:
        products_menu = wait_and_find_element(driver, By.CSS_SELECTOR, "#menu-item-product.menu-item.menu-accordion")
        products_menu.click()
        wait_and_find_element(driver, By.CSS_SELECTOR, "#menu-item-product .menu-sub.menu-sub-accordion.show")
        list_product_link = wait_and_find_element(driver, By.CSS_SELECTOR, "a.menu-link[href='https://merchant.hasaki.vn/product']")
        list_product_link.click()
        wait_and_find_element(driver, By.ID, "download_product_excel_btn")
        return True
    except TimeoutException as e:
        print(f"Navigation failed - Timeout: {str(e)}")
        return False


def download_excel(driver, download_path: str):
    try:
        download_button = wait_and_find_element(driver, By.ID, "download_product_excel_btn")

        download_button.click()

        downloaded_files = os.listdir(download_path)
        excel_file = None
        for file in downloaded_files:
            if file.endswith(".xlsx"):
                excel_file = os.path.join(download_path, file)
                break

        if excel_file:
            print(f"Excel file downloaded successfully: {excel_file}")
            return excel_file
        else:
            print("Excel file not found in the download directory.")
            return None

    except Exception as e:
        print(f"Failed to download Excel file: {str(e)}")
        return None

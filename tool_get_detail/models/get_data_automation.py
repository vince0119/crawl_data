import time
from . import setup_logger
from .database import setup_database, get_skus_by_brand_name, save_product_detail, save_market_prices, delete_existing_market_prices, check_product_exists
from .login import login
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from .selenium_helpers import wait_and_find_element


class DataAutomation:
    def __init__(self, username: str, password: str, db_config: dict, brand_name: str):
        self.username = username
        self.password = password
        self.db_config = db_config
        self.brand_name = brand_name
        self.logger = setup_logger()

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)

    def crawl_product_detail(self, url: str):
        self.driver.get(url)

        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "kt_tab_pane_4"))
            )
        except Exception as e:
            self.logger.error(f"Error loading the page: {e}")

        try:
            product_data = {
                "name": self.driver.find_element(By.ID, "name").get_attribute("value"),
                "vendor_name": self.driver.find_element(By.ID, "venprod_name").get_attribute("value"),
                "sku": self.driver.find_element(By.ID, "sku").get_attribute("value"),
                "barcode": self.driver.find_element(By.ID, "barcode").get_attribute("value"),
                "brand_name": self.driver.find_element(By.ID, "brand_name").get_attribute("value"),
                "vendor_product_code": self.driver.find_element(By.ID, "venprod_code").get_attribute("value"),
                "vendor_price": self.driver.find_element(By.ID, "venprod_price").get_attribute("value"),
                "hasaki_price": self.driver.find_element(By.ID, "price").get_attribute("value"),
                "weight": self.driver.find_element(By.ID, "weight").get_attribute("value"),
                "length": self.driver.find_element(By.ID, "plength").get_attribute("value"),
                "width": self.driver.find_element(By.ID, "width").get_attribute("value"),
                "height": self.driver.find_element(By.ID, "height").get_attribute("value"),
                "shelf_life": self.driver.find_element(By.ID, "product_shelf_life_month").get_attribute("value"),
                "expiration_date": self.driver.find_element(By.ID, "product_expiration_date_format").get_attribute(
                    "value"),
                "shelf_life_percent_po": self.driver.find_element(By.ID, "product_shelf_life_percent_po").get_attribute(
                    "value"),
            }

            return product_data
        except Exception as e:
            self.logger.error(f"Error extracting product details: {e}")

    def save_product_detail(self, product_data):
        try:
            save_product_detail(self.db_config, product_data)
        except Exception as e:
            self.logger.error(f"Error saving product details: {e}")

    def crawl_market_price(self, sku: str):
        try:
            time.sleep(5)
            table = wait_and_find_element(self.driver, By.ID, "table_id")

            rows = table.find_elements(By.TAG_NAME, "tr")
            data = []

            for row in rows[1:]:
                cols = row.find_elements(By.TAG_NAME, "td")
                if len(cols) >= 4:
                    shop_name = cols[1].text.strip()
                    price_text = cols[2].text.strip()
                    url = cols[3].find_element(By.TAG_NAME, 'a').get_attribute('href').strip()
                    price = int(price_text.replace("₫", "").replace(".", "").replace(",", "").strip())

                    data.append({
                        'shop_name': shop_name,
                        'price': price,
                        'url': url
                    })

            if data:
                self.save_market_prices(sku, data)

            return data
        except Exception as e:
            self.logger.error(f"Error crawling market price: {e}")

    def save_market_prices(self, sku: str, market_prices: list):
        try:
            delete_existing_market_prices(self.db_config, sku)

            if market_prices:
                save_market_prices(self.db_config, sku, market_prices)
            else:
                self.logger.warning(f"No market prices to save for SKU: {sku}")

        except Exception as e:
            self.logger.error(f"Error in save_market_prices for SKU {sku}: {str(e)}")

    def run(self):
        try:
            if not setup_database(self.db_config):
                raise Exception("Database setup failed - check database connection details")

            if not login(self.driver, self.username, self.password):
                raise Exception("Login failed - check credentials")

            skus = get_skus_by_brand_name(self.db_config, self.brand_name)

            if not skus:
                self.logger.warning(f"No SKUs found for brand: {self.brand_name}")
                return

            for index, sku in enumerate(skus, 1):
                try:
                    url = f"https://merchant.hasaki.vn/product/edit-sku/{sku}?vendor=210"

                    if check_product_exists(self.db_config, sku):
                        self.logger.info(f"SKU {sku} already exists in the database. Deleting existing market prices.")
                        delete_existing_market_prices(self.db_config, sku)

                    product_data = self.crawl_product_detail(url)
                    if not product_data:
                        self.logger.warning(f"Skipping SKU {sku} due to missing product details.")
                        continue

                    self.save_product_detail(product_data)

                    market_prices = self.crawl_market_price(sku)
                    if not market_prices:
                        self.logger.warning(f"No market prices found for SKU {sku}.")
                        continue

                    self.save_market_prices(sku, market_prices)

                except Exception as sku_error:
                    self.logger.error(f"Error processing SKU {sku}: {str(sku_error)}")

        except Exception as e:
            self.logger.error(f"Automation process failed: {str(e)}")
        finally:
            self.driver.quit()

from . import setup_logger
from .database import setup_database, save_to_database
from .login import login
from .product import navigate_to_product_page, download_excel
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class HasakiAutomation:
    def __init__(self, username: str, password: str, db_config: dict, download_path: str):
        self.username = username
        self.password = password
        self.db_config = db_config
        self.download_path = download_path
        self.logger = setup_logger()

        chrome_options = Options()
        chrome_options.add_argument('--headless')

        self.driver = webdriver.Chrome(options=chrome_options)

    def run(self):
        try:
            if not setup_database(self.db_config):
                raise Exception("Database setup failed")

            if not login(self.driver, self.username, self.password):
                raise Exception("Login failed")

            if not navigate_to_product_page(self.driver):
                raise Exception("Navigation to product page failed")

            excel_file = download_excel(self.driver, self.download_path)
            if not excel_file:
                raise Exception("Excel download failed")

            if not save_to_database(excel_file, self.db_config):
                raise Exception("Saving to database failed")

            self.logger.info("Automation process completed successfully")

        except Exception as e:
            self.logger.error(f"Automation process failed: {str(e)}")
        finally:
            self.driver.quit()

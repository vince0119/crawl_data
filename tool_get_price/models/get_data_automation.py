from . import setup_logger
import json
from selenium import webdriver
from .database import get_url_by_shop_name, save_product_data
from .crawl_data import crawl_data_from_boshop, crawl_data_from_watson, crawl_data_from_skinfood, \
    crawl_data_from_sociolla, crawl_data_from_cocolux, crawl_data_from_abbeautyworld, crawl_data_from_guardian, \
    crawl_data_from_lamthao, crawl_data_from_mint07, crawl_data_from_beautybox, crawl_data_from_sammi
from typing import Union, List


class DataAutomation:
    def __init__(self, db_config: dict, shop_names: Union[str, List[str]]):
        self.db_config = db_config
        self.shop_names = shop_names if isinstance(shop_names, list) else [shop_names]
        self.logger = setup_logger()

        options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=options)

    @staticmethod
    def load_shop_name_from_config(config_file: str) -> List[str]:
        with open(config_file, 'r') as file:
            config = json.load(file)
        return config.get("shop_name", [])

    def save_product_data(self, product_data):
        if not save_product_data(self.db_config, product_data):
            self.logger.error("Failed to save product data for URL: %s", product_data['url'])

    def run(self):
        try:
            for shop_name in self.shop_names:
                urls = get_url_by_shop_name(self.db_config, shop_name)
                for url in urls:
                    try:
                        product_data = self._crawl_product_data(shop_name, url)
                        if product_data:
                            self.save_product_data(product_data)
                    except Exception as crawl_error:
                        self.logger.error(f"Error crawling {url} from {shop_name}: {crawl_error}")

        except Exception as e:
            self.logger.error(f"Error running the bot: {e}")
        finally:
            self.driver.quit()

    def _crawl_product_data(self, shop_name: str, url: str):
        crawl_functions = {
            "watsons.vn": crawl_data_from_watson,
            "boshop.vn": crawl_data_from_boshop,
            "thegioiskinfood.com": crawl_data_from_skinfood,
            "vn.sociolla.com": crawl_data_from_sociolla,
            "cocolux.com": crawl_data_from_cocolux,
            "abbeautyworld.com": crawl_data_from_abbeautyworld,
            "guardian.com.vn": crawl_data_from_guardian,
            "lamthaocosmetics.vn": crawl_data_from_lamthao,
            "mint07.com": crawl_data_from_mint07,
            "beautybox.com.vn": crawl_data_from_beautybox,
            "sammishop.com": crawl_data_from_sammi
        }

        crawl_func = crawl_functions.get(shop_name)
        if crawl_func:
            return crawl_func(self.driver, url)

        self.logger.error(f"No crawling function for shop: {shop_name}")
        return None
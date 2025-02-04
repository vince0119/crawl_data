import re
from .selenium_helpers import wait_and_find_element
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def clean_price(price_str: str) -> int:
    price_str = re.sub(r'[^\d]', '', price_str)
    return int(price_str) if price_str else 0


def clean_discount(discount_str: str) -> int:
    match = re.search(r'-?\d+', discount_str)
    return int(match.group(0)) if match else 0


def crawl_data_from_watson(driver, url: str):
    driver.get(url)
    product_data = {
        "price_in_website": 0,
        "retail_price": 0,
        "discount": 0,
        "url": url,
        "website_status": "OK"
    }

    try:
        price_summary = wait_and_find_element(driver, By.CSS_SELECTOR, ".price-summary")

        price_element = price_summary.find_elements(By.CSS_SELECTOR, ".display-price .price")
        product_data["price_in_website"] = clean_price(price_element[0].text) if price_element else 0

        retail_price_element = price_summary.find_elements(By.CSS_SELECTOR, ".recommended-retail-price .retail-price")
        product_data["retail_price"] = clean_price(retail_price_element[0].text) if retail_price_element else 0

        discount_element = price_summary.find_elements(By.CSS_SELECTOR, ".display-price .discount")
        product_data["discount"] = clean_discount(discount_element[0].text) if discount_element else 0

        if (product_data["price_in_website"] == 0 and
                product_data["retail_price"] == 0 and
                product_data["discount"] == 0):
            product_data["website_status"] = "404 NOT FOUND"

    except (TimeoutException, NoSuchElementException):
        product_data["website_status"] = "404"

    return product_data


def crawl_data_from_boshop(driver, url: str):
    driver.get(url)
    product_data = {
        "price_in_website": 0,
        "retail_price": 0,
        "discount": 0,
        "url": url,
        "website_status": "OK"
    }
    try:
        price_summary = wait_and_find_element(driver, By.CSS_SELECTOR, ".price.z")

        price = price_summary.find_element(By.CSS_SELECTOR, ".item-price span").text
        product_data["price_in_website"] = clean_price(price[0].text) if price else 0

        retail_price = price_summary.find_element(By.CSS_SELECTOR, ".item-price.second.second2 span")
        product_data["retail_price"] = clean_price(retail_price[0].text) if retail_price else 0

        discount = price_summary.find_element(By.CSS_SELECTOR, ".item-price.second.second3 span")
        product_data["discount"] = clean_discount(discount[0].text) if discount else 0

        if (product_data["price_in_website"] == 0 and
                product_data["retail_price"] == 0 and
                product_data["discount"] == 0):
            product_data["website_status"] = "404 NOT FOUND"

    except (TimeoutException, NoSuchElementException):

        product_data["website_status"] = "404"

    return product_data


def crawl_data_from_skinfood(driver, url: str):
    driver.get(url)
    product_data = {
        "price_in_website": 0,
        "retail_price": 0,
        "discount": 0,
        "url": url,
        "website_status": "OK"
    }

    try:
        price_summary = wait_and_find_element(driver, By.CSS_SELECTOR, ".page-product-info-pricewrap")
        discount_header = wait_and_find_element(driver, By.CSS_SELECTOR, ".page-product-info-badge")

        price = price_summary.find_elements(By.CSS_SELECTOR, ".page-product-info-newprice span")
        product_data["price_in_website"] = clean_price(price[0].text) if price else 0
        print('Price: ', product_data["price_in_website"])

        retail_price = price_summary.find_elements(By.CSS_SELECTOR, ".page-product-info-oldprice span")
        product_data["retail_price"] = clean_price(retail_price[0].text) if retail_price else 0

        discount = discount_header.find_element(By.CSS_SELECTOR, ".page-product-info-badge-discount")
        product_data["discount"] = clean_discount(discount.text) if discount else 0

        if (product_data["price_in_website"] == 0 and
                product_data["retail_price"] == 0):
            product_data["website_status"] = "404 NOT FOUND"

    except (TimeoutException, NoSuchElementException):
        product_data["website_status"] = "404"

    return product_data


def crawl_data_from_sociolla(driver, url: str):
    driver.get(url)
    product_data = {
        "price_in_website": 0,
        "retail_price": 0,
        "discount": 0,
        "url": url,
        "website_status": "OK"
    }

    try:
        price_summary = wait_and_find_element(driver, By.CSS_SELECTOR, ".left-content.container-top-mobile")

        price = price_summary.find_elements(By.CSS_SELECTOR, ".price-display-top li span")
        product_data["price_in_website"] = clean_price(price[0].text) if price else 0

        retail_price = price_summary.find_elements(By.CSS_SELECTOR, ".info.clearfix.mb-20 li .save")
        product_data["retail_price"] = clean_price(retail_price[0].text) if retail_price else 0

        if (product_data["price_in_website"] == 0 and
                product_data["retail_price"] == 0):
            product_data["website_status"] = "404 NOT FOUND"

    except (TimeoutException, NoSuchElementException):
        product_data["website_status"] = "404"

    return product_data


def crawl_data_from_cocolux(driver, url: str):
    driver.get(url)
    product_data = {
        "price_in_website": 0,
        "retail_price": 0,
        "discount": 0,
        "url": url,
        "website_status": "OK"
    }

    try:
        price_summary = wait_and_find_element(driver, By.CSS_SELECTOR, ".detail-price")

        price = price_summary.find_elements(By.CSS_SELECTOR, ".public-price span")
        product_data["price_in_website"] = clean_price(price[0].text) if price else 0

        retail_price = price_summary.find_elements(By.CSS_SELECTOR, ".origin-price span:first-child")
        product_data["retail_price"] = clean_price(retail_price[0].text) if retail_price else 0

        discount = price_summary.find_elements(By.CSS_SELECTOR, ".origin-price span:nth-child(3)")
        product_data["discount"] = clean_discount(discount[0].text) if discount else 0

        if (product_data["price_in_website"] == 0 and
                product_data["retail_price"] == 0 and
                product_data["discount"] == 0):
            product_data["website_status"] = "404 NOT FOUND"

    except (TimeoutException, NoSuchElementException):
        product_data["website_status"] = "404"

    return product_data


def crawl_data_from_abbeautyworld(driver, url: str):
    driver.get(url)
    product_data = {
        "price_in_website": 0,
        "retail_price": 0,
        "discount": 0,
        "url": url,
        "website_status": "OK"
    }

    try:
        price_summary = wait_and_find_element(driver, By.CSS_SELECTOR, ".product-price")

        price = price_summary.find_elements(By.CSS_SELECTOR, ".current-price .pro-price")
        product_data["price_in_website"] = clean_price(price[0].text) if price else 0

        retail_price = price_summary.find_elements(By.CSS_SELECTOR, ".price-compare .com-price")
        product_data["retail_price"] = clean_price(retail_price[0].text) if retail_price else 0

        discount = price_summary.find_elements(By.CSS_SELECTOR, ".price-compare .percent-save")
        product_data["discount"] = clean_discount(discount[0].text) if discount else 0

        if (product_data["price_in_website"] == 0 and
                product_data["retail_price"] == 0 and
                product_data["discount"] == 0):
            product_data["website_status"] = "404 NOT FOUND"

    except (TimeoutException, NoSuchElementException):
        product_data["website_status"] = "404"

    return product_data


def crawl_data_from_guardian(driver, url: str):
    driver.get(url)
    product_data = {
        "price_in_website": 0,
        "retail_price": 0,
        "discount": 0,
        "url": url,
        "website_status": "OK"
    }

    try:
        price_summary = wait_and_find_element(driver, By.CSS_SELECTOR, ".price-final_price")

        price = price_summary.find_elements(By.CSS_SELECTOR, ".special-price .price")
        product_data["price_in_website"] = clean_price(price[0].text) if price else 0

        retail_price = price_summary.find_elements(By.CSS_SELECTOR, ".old-price .price")
        product_data["retail_price"] = clean_price(retail_price[0].text) if retail_price else 0

        discount = price_summary.find_elements(By.CSS_SELECTOR, ".percent-discount")
        product_data["discount"] = clean_discount(discount[0].text) if discount else 0

        if (product_data["price_in_website"] == 0 and
                product_data["retail_price"] == 0 and
                product_data["discount"] == 0):
            product_data["website_status"] = "404 NOT FOUND"

    except (TimeoutException, NoSuchElementException):
        product_data["website_status"] = "404"

    return product_data


def crawl_data_from_lamthao(driver, url: str):
    driver.get(url)
    product_data = {
        "price_in_website": 0,
        "retail_price": 0,
        "discount": 0,
        "url": url,
        "website_status": "OK"
    }

    try:
        price_summary = wait_and_find_element(driver, By.CSS_SELECTOR, ".finpricezicgr")

        price = price_summary.find_elements(By.CSS_SELECTOR, ".pricenetold")
        product_data["price_in_website"] = clean_price(price[0].text) if price else 0

        retail_price = price_summary.find_elements(By.CSS_SELECTOR, ".pricenet")
        product_data["retail_price"] = clean_price(retail_price[0].text) if retail_price else 0

        discount = price_summary.find_elements(By.CSS_SELECTOR, ".finpricezicgr21")
        product_data["discount"] = clean_discount(discount[0].text) if discount else 0

        if (product_data["price_in_website"] == 0 and
                product_data["retail_price"] == 0 and
                product_data["discount"] == 0):
            product_data["website_status"] = "404 NOT FOUND"

    except (TimeoutException, NoSuchElementException):
        product_data["website_status"] = "404"

    return product_data


def crawl_data_from_mint07(driver, url: str):
    driver.get(url)
    website_status = "OK"
    product_data = {}
    try:
        price_summary = wait_and_find_element(driver, By.CSS_SELECTOR, ".price")
        discount_summary = wait_and_find_element(driver, By.CSS_SELECTOR, ".product-images-wrapper")
        if price_summary:
            price_elements = price_summary.find_elements(By.CSS_SELECTOR, ".woocommerce-Price-amount.amount bdi")
            discount = discount_summary.find_elements(By.CSS_SELECTOR, ".percentage")

            if len(price_elements) == 1:
                price = price_elements[0].text
                retail_price = price
            elif len(price_elements) == 2:
                price = price_elements[0].text
                retail_price = price_elements[1].text
            else:
                website_status = "404 NOT FOUND"
                return {
                    "price_in_website": 0,
                    "retail_price": 0,
                    "discount": 0,
                    "url": url,
                    "website_status": website_status
                }

            product_data = {
                "price_in_website": clean_price(price) if price else 0,
                "retail_price": clean_price(retail_price) if retail_price else 0,
                "discount": clean_discount(discount) if discount else 0,
                "url": url,
                "website_status": website_status
            }

    except TimeoutException:
        print("Failed to retrieve price data for %s", url)

    return product_data


def crawl_data_from_beautybox(driver, url: str):
    driver.get(url)
    product_data = {
        "price_in_website": 0,
        "retail_price": 0,
        "discount": 0,
        "url": url,
        "website_status": "OK"
    }

    try:
        price_summary = wait_and_find_element(driver, By.CSS_SELECTOR, ".space-between")

        price = price_summary.find_elements(By.CSS_SELECTOR, ".ant-space-item span:first-child")
        product_data["price_in_website"] = clean_price(price[0].text) if price else 0

        retail_price = price_summary.find_elements(By.CSS_SELECTOR, ".ant-space-item .line-through")
        product_data["retail_price"] = clean_price(retail_price[0].text) if retail_price else 0

        discount = price_summary.find_elements(By.CSS_SELECTOR, ".ant-space-item .price")
        product_data["discount"] = clean_discount(discount[0].text) if discount else 0

        if (product_data["price_in_website"] == 0 and
                product_data["retail_price"] == 0 and
                product_data["discount"] == 0):
            product_data["website_status"] = "404 NOT FOUND"

    except (TimeoutException, NoSuchElementException):
        product_data["website_status"] = "404"

    return product_data


def crawl_data_from_sammi(driver, url: str):
    driver.get(url)
    product_data = {
        "price_in_website": 0,
        "retail_price": 0,
        "discount": 0,
        "url": url,
        "website_status": "OK"
    }
    try:
        modal = wait_and_find_element(driver, By.CSS_SELECTOR, ".modal.fade.show")

        close_button = modal.find_element(By.CSS_SELECTOR, ".btn-form-close.close")
        close_button.click()
    except TimeoutException:
        print("No modal found or unable to close")

    try:
        price_element = wait_and_find_element(driver, By.CSS_SELECTOR, ".price-box .special-price .price.product-price")
        # price = price_element.find_elements()
        product_data["price_in_website"] = clean_price(price_element.text) if price_element else 0

        retail_price_element = driver.find_elements(By.CSS_SELECTOR, ".price-box .old-price .price.product-price-old")
        product_data["retail_price"] = clean_price(retail_price_element[0].text) if retail_price_element else 0

        discount_element = driver.find_elements(By.CSS_SELECTOR, "div.price-box .label_product")
        product_data["discount"] = clean_discount(discount_element[0].text) if discount_element else 0

        if (product_data["price_in_website"] == 0 and
                product_data["retail_price"] == 0 and
                product_data["discount"] == 0):
            product_data["website_status"] = "404 NOT FOUND"

    except (TimeoutException, NoSuchElementException):
        product_data["website_status"] = "404"

    return product_data

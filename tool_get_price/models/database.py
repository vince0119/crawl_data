from contextlib import contextmanager
import psycopg2
from datetime import datetime
from typing import Dict, List, Generator, Union


@contextmanager
def get_db_connection(db_config: Dict) -> Generator:
    conn = psycopg2.connect(**db_config)
    try:
        yield conn
    finally:
        conn.close()


def get_url_by_shop_name(db_config: Dict, shop_names: Union[str, List[str]]) -> List[str]:
    with get_db_connection(db_config) as conn:
        with conn.cursor() as cursor:
            if isinstance(shop_names, str):
                shop_names = [shop_names]

            cursor.execute(
                'SELECT url FROM market_price WHERE shop_name = ANY(%s)',
                (shop_names,)
            )
            return [row[0] for row in cursor.fetchall()]


def save_product_data(db_config: Dict, product_data: Dict) -> bool:
    with get_db_connection(db_config) as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                UPDATE market_price 
                SET 
                    price_in_website = %(price_in_website)s,
                    retail_price = %(retail_price)s,
                    discount = %(discount)s,
                    updated_at = %(updated_at)s,
                    website_status = %(website_status)s
                WHERE url = %(url)s
            ''', {**product_data, 'updated_at': datetime.now()})
            conn.commit()
            return cursor.rowcount > 0
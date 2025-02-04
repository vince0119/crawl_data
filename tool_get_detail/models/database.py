import psycopg2


def setup_database(db_config):
    try:
        # Connect to the database
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS product_detail ( 
                id SERIAL PRIMARY KEY, 
                sku VARCHAR(255) UNIQUE, 
                barcode VARCHAR(255), 
                name TEXT, 
                brand_name VARCHAR(255), 
                vendor_name VARCHAR(255), 
                venprod_code VARCHAR(255), 
                venprod_price INTEGER, 
                hasaki_price INTEGER, 
                weight FLOAT, 
                length FLOAT, 
                width FLOAT, 
                height FLOAT, 
                shelf_life INTEGER, 
                expiration_date DATE, 
                shelf_life_percent_po INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
            ) 
        ''')

        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS market_price (
                id SERIAL PRIMARY KEY,
                sku VARCHAR(255),
                shop_name VARCHAR(255),
                price INTEGER,
                url TEXT,
                price_in_website INTEGER,
                retail_price INTEGER,
                discount INTEGER,
                website_status VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP,
                FOREIGN KEY (sku) REFERENCES product_detail(sku) ON DELETE CASCADE
            )
        ''')

        conn.commit()
        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"Database setup failed: {str(e)}")
        return False


def get_skus_by_brand_name(db_config, brand_name: str):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute(''' 
            SELECT sku FROM product
            WHERE brand_name = %s
        ''', (brand_name,))

        skus = [row[0] for row in cursor.fetchall()]
        conn.close()
        return skus

    except Exception as e:
        print(f"Database query failed: {str(e)}")
        return []


def save_product_detail(db_config, product_data):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        vendor_price = int(product_data['vendor_price'].replace(',', ''))
        hasaki_price = int(product_data['hasaki_price'].replace(',', ''))
        shelf_life = int(product_data['shelf_life'])
        shelf_life_percent_po = int(product_data['shelf_life_percent_po'])
        weight = float(product_data['weight']) if product_data['weight'] else 0.0
        length = float(product_data['length']) if product_data['length'] else 0.0
        width = float(product_data['width']) if product_data['width'] else 0.0
        height = float(product_data['height']) if product_data['height'] else 0.0

        insert_query = """
        INSERT INTO product_detail (
            sku, name, venprod_name, barcode, brand, venprod_code, 
            venprod_price, hasaki_price, weight, length, width, height, 
            shelf_life_month, expiration_date_format, shelf_life_percent_po
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            product_data['sku'],
            product_data['name'],
            product_data['vendor_name'],
            product_data['barcode'],
            product_data['brand_name'],
            product_data['vendor_product_code'],
            vendor_price,
            hasaki_price,
            weight,
            length,
            width,
            height,
            shelf_life,
            product_data['expiration_date'],
            shelf_life_percent_po
        ))

        conn.commit()
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error saving product details: {e}")


def save_market_prices(db_config, sku: str, market_prices: list):
    try:
        with psycopg2.connect(**db_config) as conn:
            with conn.cursor() as cursor:
                insert_query = """
                    INSERT INTO market_price (sku, shop_name, price, url)
                    VALUES (%s, %s, %s, %s)
                    """

                for price_data in market_prices:
                    cursor.execute(insert_query, (
                        sku,
                        price_data.get('shop_name', ''),
                        price_data.get('price', ''),
                        price_data.get('url', '')
                    ))

        return True
    except Exception as e:
        print(f"Error saving market prices: {e}")


def delete_existing_market_prices(db_config, sku: str):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        delete_query = "DELETE FROM market_price WHERE sku = %s"
        cursor.execute(delete_query, (sku,))
        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting existing market prices: {e}")


def check_product_exists(db_config, sku: str):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute("SELECT EXISTS(SELECT 1 FROM product_detail WHERE sku = %s)", (sku,))
        exists = cursor.fetchone()[0]

        cursor.close()
        conn.close()
        return exists
    except Exception as e:
        print(f"Error checking product existence: {e}")

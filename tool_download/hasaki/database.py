import psycopg2
from psycopg2.extras import Json
from datetime import datetime
import os


def setup_database(db_config):
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS product ( 
                id INTEGER PRIMARY KEY, 
                sku VARCHAR(255), 
                barcode VARCHAR(255), 
                name TEXT, 
                brand_name VARCHAR(255), 
                price INTEGER, 
                hasaki_price INTEGER, 
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
            ) 
        ''')

        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS product_detail (
                id SERIAL PRIMARY KEY,
                sku VARCHAR(255) UNIQUE,
                name VARCHAR(255),
                venprod_name VARCHAR(255),
                barcode VARCHAR(255),
                brand VARCHAR(255),
                venprod_code VARCHAR(50),
                venprod_price INTEGER,
                hasaki_price INTEGER,
                weight FLOAT,
                length FLOAT,
                width FLOAT,
                height FLOAT,
                shelf_life_month INT,
                expiration_date_format VARCHAR(50),
                shelf_life_percent_po INT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS excel_file (
                id SERIAL PRIMARY KEY,
                filename VARCHAR(255) NOT NULL,
                download_date TIMESTAMP NOT NULL,
                file_path VARCHAR(255) NOT NULL,
                data_json JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        conn.commit()
        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"Database setup failed: {str(e)}")
        return False


def save_to_database(file_path, db_config):
    try:
        import pandas as pd
        df = pd.read_excel(file_path, skiprows=2, engine="openpyxl")

        if '#' in df.columns:
            df = df.rename(columns={'#': 'id'})

        df.columns = [col.lower().strip().replace(' ', '_') for col in df.columns]

        df['hasaki_price'] = df['hasaki_price'].apply(lambda x: 0 if str(x).strip() in ['-', 'Blank'] else x)
        df['barcode'] = df['barcode'].apply(lambda x: 0 if str(x).strip() in ['-', 'Blank'] else x)

        df['hasaki_price'] = pd.to_numeric(df['hasaki_price'], errors='coerce').fillna(0).astype(int)
        df['barcode'] = pd.to_numeric(df['barcode'], errors='coerce').fillna(0).astype(int)

        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        for index, row in df.iterrows():
            cursor.execute('''
                INSERT INTO product (id, sku, barcode, name, brand_name, price, hasaki_price)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    sku = EXCLUDED.sku,
                    barcode = EXCLUDED.barcode,
                    name = EXCLUDED.name,
                    brand_name = EXCLUDED.brand_name,
                    price = EXCLUDED.price,
                    hasaki_price = EXCLUDED.hasaki_price
            ''', (
                int(row['id']),
                str(row['sku']),
                int(row['barcode']),
                str(row['name']),
                str(row['brand_name']),
                float(str(row['price']).replace(',', '')) if row['price'] else None,
                float(row['hasaki_price']) if row['hasaki_price'] is not None else 0
            ))

        cursor.execute('''
            INSERT INTO excel_file (filename, download_date, file_path, data_json)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        ''', (
            os.path.basename(file_path),
            datetime.now(),
            file_path,
            Json(df.to_dict(orient='records'))
        ))

        conn.commit()
        cursor.close()
        conn.close()

        return True
    except Exception as e:
        print(f"Database save failed: {str(e)}")
        return False

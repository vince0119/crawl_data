from models.get_data_automation import DataAutomation
import json
from pathlib import Path


def load_config(config_path: Path = Path("config.json")) -> dict:
    try:
        return json.loads(config_path.read_text())
    except Exception as e:
        print(f"Error loading config: {e}")
        return {}


if __name__ == "__main__":
    db_config = {
        "host": "18.237.216.23",
        "port": "5432",
        "dbname": "shopee_db",
        "user": "admin",
        "password": "1234"
    }

    config = load_config()
    shop_names = config.get("shop_name", [])

    if not shop_names:
        raise ValueError("Shop name is not configured")

    bot = DataAutomation(
        db_config=db_config,
        shop_names=shop_names
    )
    bot.run()

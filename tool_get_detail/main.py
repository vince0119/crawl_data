import json
from models.get_data_automation import DataAutomation


def load_config(config_path="config.json"):
    try:
        with open(config_path, "r") as config_file:
            config = json.load(config_file)
        return config
    except Exception as e:
        return {}


if __name__ == "__main__":
    db_config = {
        "dbname": "shopee_db",
        "user": "test_website",
        "password": "1234"
    }

    config = load_config()
    brand_name = config.get("brand_name", "")

    if not brand_name:
        print("Brand name is not configured. Exiting...")
    else:
        bot = DataAutomation(
            username="tuan.nguyen@tinvietcosmetic.com",
            password="TV@hasaki2024",
            db_config=db_config,
            brand_name=brand_name
        )
        bot.run()

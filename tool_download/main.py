from hasaki.hasaki_automation import HasakiAutomation

if __name__ == "__main__":
    db_config = {
        "host": "18.237.216.23",
        "port": "5432",
        "dbname": "shopee_db",
        "user": "admin",
        "password": "1234"
    }

    download_path = "./downloads"

    bot = HasakiAutomation(
        username="tuan.nguyen@tinvietcosmetic.com",
        password="TV@hasaki2024",
        db_config=db_config,
        download_path=download_path
    )
    bot.run()

from hasaki.hasaki_automation import HasakiAutomation

if __name__ == "__main__":
    db_config = {
        "dbname": "shopee_db",
        "user": "test_website",
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

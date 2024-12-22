import os

try:
    data_path = os.getenv("MY_PC_DATA_PATH")

    bot_token_file = open(data_path + "bot_token.txt", "r")
    BOT_TOKEN = bot_token_file.read()
    bot_token_file.close()

    telegram_ids_file = open(data_path + "users.txt", "r")
    TELEGRAM_IDS = [int(id) for id in telegram_ids_file.read().split(",")]
    telegram_ids_file.close()

except:
    from plyer import notification
    notification.notify(
        title="Хм... Данные не были найдены",
        message="Довавьте данные в приложении для настройки MyComputer",
        app_name="MyComputer",
    )

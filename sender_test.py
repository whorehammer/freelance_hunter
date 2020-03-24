from telethon.sync import TelegramClient
import logging
from database_interface import AdminInteraction
from config_app import owner_list, Config
import time

api_id = 1  # tour api id
api_hash = ""  # your api hash
session_name = "fh"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

client = TelegramClient(session_name, api_id, api_hash)
client.start()


def main():
    admin = AdminInteraction(owner_list)
    message = admin.get_message_from_db(owner_list[0])
    for dialog in client.get_dialogs():
        if hasattr(dialog.entity, 'megagroup'):
            if dialog.entity.megagroup:
                time.sleep(Config.wait_before_send)
                print(dialog.entity.title)
                try:
                    client.send_message(dialog, message=message)
                except Exception as e:
                    print(e)
                    continue


if __name__ == "__main__":
    main()



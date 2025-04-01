from db_hand import create_db
from vk_bot_handler import bot_handler

if __name__ == '__main__':

    create_db()
    start_bot = bot_handler()

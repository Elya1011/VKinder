import configparser
import os

from db_hand import create_db, adding_favorite_users
from functions import VkBot
from time import sleep

from vk_bot import bot_handler

if __name__ == '__main__':

    create_db()
    start_bot = bot_handler()
    vk_session = VkBot(access_token=os.getenv('VKTOKEN'))

    # Передать данные запроса из бота
    search_result = vk_session.search_users(age_from=18, age_to=25, sex=1, city='Москва')

    for profile in search_result:

        profile_id = profile['id']
        profile_name = f'{profile["first_name"]} {profile["last_name"]}'
        profile_link = f'https://vk.com/id{profile["id"]}'
        pics_list = vk_session.get_photo_links(user_id=profile['id'])
        print(profile_id, profile_name, profile_link)

        # adding_favorite_users(profile_id, profile_name, profile_link, pics_list[0])

        sleep(0.1)
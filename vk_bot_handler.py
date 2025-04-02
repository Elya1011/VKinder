import vk_api, os, json

from db_hand import save_user_id, adding_favorite_users, adding_dark_list, display_of_favorite_users
from functions import VkBot
from keyboards import keyboard_2, keyboard_1
from dotenv import load_dotenv
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
load_dotenv()
# Настройки
GROUP_ID = 229695508  # Число, например 12345678
TOKEN = os.getenv('VK_BOT_TOKEN')  # Строка из настроек сообщества

# Авторизация
vk_session = vk_api.VkApi(token=TOKEN)
backend_session = VkBot(access_token=os.getenv('VKTOKEN'))
longpoll = VkBotLongPoll(vk_session, group_id=GROUP_ID)
vk = vk_session.get_api()

search_request = {'age_from': 18, 'age_to': 50, 'sex': 0, 'city': 'Москва'}

def standard_keyboard_message(user_id, text):
    vk.messages.send(
        user_id=user_id,
        message=text,
        random_id=0
    )

def send_message(user_id, message):
    keyboard = {
        'inline': False,
        "one_time": True,
        "buttons": [
            [
                {
                    'action': {
                        'type': 'text',
                        'label': 'мужчины'
                    },
                    'color': 'positive'
                },
                {
                    'action': {
                        'type': 'text',
                        'label': 'девушки'
                    },
                    'color': 'positive'
                }

            ]
        ]
    }
    vk.messages.send(
        user_id=user_id,
        message=message,
        random_id=0,  # Уникальный идентификатор сообщения
        keyboard=json.dumps(keyboard)
    )

def message_2(user_id, message):
    vk.messages.send(
        user_id=user_id,
        message=message,
        random_id=0,  # Уникальный идентификатор сообщения
        keyboard=json.dumps(keyboard_2)
    )


def display_result_message(user_id: int, message: str, attachments: list = None):
    params = {
        'user_id': user_id,
        'message': message,
        'random_id': 0,
        'keyboard': json.dumps(keyboard_1)
    }
    if attachments:  # Добавляем attachment только если есть вложения
        params['attachment'] = ','.join(attachments)
    print(params)
    vk.messages.send(**params)

def bot_handler():
    """Логика взаимодействия пользователя с ботом. Вызывается в bot_main"""
    user_states = {}
    user_search_results = {}
    print('бот работает')

    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            msg = event.object.message
            user_id = msg['from_id']
            text = msg['text'].lower()
            save_user_id(user_id)
            print(text)

            if text in ['старт', 'закончить поиск🚫']:
                send_message(user_id, 'Привет! Выберите пол')

            elif text == 'девушки' or text == 'мужчины':
                message_2(user_id, 'Выберите нужный диапазон возраста')
                if text == 'девушки':
                    search_request['sex'] = 1
                if text == 'мужчины':
                    search_request['sex'] = 2

            elif text in ['18-25', '26-30', '31-40', '41-50']:
                search_request['age_from'] = int(text.split('-')[0])
                search_request['age_to'] = int(text.split('-')[1])
                standard_keyboard_message(user_id, 'Введите город для поиска')
                user_states[user_id] = "waiting_for_input"

            elif user_id in user_states and user_states[user_id] == "waiting_for_input":
                search_request['city'] = text
                del user_states[user_id]
                user_search_results[user_id] = backend_session.search_users(**search_request)
                user_states[user_id] = 0
                current_result = user_search_results[user_id][user_states[user_id]]
                message = f"{current_result['first_name']} {current_result['last_name']} https://vk.com/id{current_result['id']}"
                attachments = backend_session.get_photo_links(
                    current_result['id']
                )
                print(attachments)
                display_result_message(user_id, message, attachments)

            elif user_id in user_states and isinstance(user_states[user_id], int) and \
            text in ["дальше👉", "👈назад"]:
                step = {"дальше👉": 1, "👈назад": -1}
                user_states[user_id] += step[text]
                current_result = user_search_results[user_id][user_states[user_id]]
                message = f"{current_result['first_name']} {current_result['last_name']} https://vk.com/id{current_result['id']}"
                attachments = backend_session.get_photo_links(
                    current_result['id']
                )
                display_result_message(user_id, message, attachments)

            elif user_id in user_states and isinstance(user_states[user_id], int) and \
            text in ["добавить в избранное"]:
                current_result = user_search_results[user_id][user_states[user_id]]
                adding_favorite_users(user_id, current_result['id'])

            elif user_id in user_states and isinstance(user_states[user_id], int) and \
            text in ["добавить в чёрный список"]:
                current_result = user_search_results[user_id][user_states[user_id]]
                adding_dark_list(user_id, current_result['id'])

            elif user_id in user_states and isinstance(user_states[user_id], int) and \
            text in ["просмотреть избранное"]:
                favourite_id_list = [f'https://vk.com/id{c}' for c in display_of_favorite_users(user_id)]
                message = '\n'.join(favourite_id_list)
                print(message)
                display_result_message(user_id, message)
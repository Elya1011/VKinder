import vk_api, os, json

from db_hand import save_user_id
from functions import VkBot
from keyboards import keyboard_2
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

# Логика взаимодействия пользователя с ботом. Вызывается в bot_main
def bot_handler():
    user_states = {}
    print('бот работает')
# Обработка событий
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            msg = event.object.message
            user_id = msg['from_id']
            text = msg['text'].lower()
            save_user_id(user_id)

            if text == 'старт':
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
                backend_session.save_search_result(search_request)


import vk_api, os, json
from keyboards import keyboard_2
from dotenv import load_dotenv
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
load_dotenv()
# Настройки
GROUP_ID = 229695508  # Число, например 12345678
TOKEN = os.getenv('VK_BOT_TOKEN')  # Строка из настроек сообщества
print(TOKEN)
# Авторизация
vk_session = vk_api.VkApi(token=TOKEN)
longpoll = VkBotLongPoll(vk_session, group_id=GROUP_ID)
vk = vk_session.get_api()

data_search = {}


def send_message(user_id, message):
    keyboard = {
        'inline': False,
        "one_time": False,
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


def bot_handler():
    print('бот работает')
# Обработка событий
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            msg = event.object.message
            user_id = msg['from_id']
            text = msg['text'].lower()

            if text == 'старт':
                send_message(user_id, 'Привет! Выберите пол')

            elif text == 'девушки' or text == 'мужчины':
                message_2(user_id, 'Выберите нужный диапазон возраста')



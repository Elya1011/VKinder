import vk_api, os, json
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


def send_message(user_id, message):
    keyboard = {
        'inline': False,
        "one_time": False,
        "buttons": [
            [
                {
                    'action': {
                        'type': 'text',
                        'label': 'Next'
                    },
                    'color': 'positive'
                },
                {
                    'action': {
                        'type': 'text',
                        'label': 'Stop'
                    },
                    'color': 'negative'
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






if __name__ == "__main__":
    print('бот работает')
# Обработка событий
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            msg = event.object.message
            user_id = msg['from_id']
            text = msg['text'].lower()

            if text == 'привет':
                send_message(user_id, 'Привет! Чем могу помочь?')
            elif text == 'пока':
                send_message(user_id, 'Пока')



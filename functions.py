import requests as r
from time import sleep
from dotenv import load_dotenv
load_dotenv()



class VkBot:
    def __init__(self, access_token, api_version=5.199):
        self.base_url = 'https://api.vk.com/method/'
        self.params = {
            'access_token': access_token,
            'v': api_version
        }

    def search_users(self, age=18, sex=0, hometown='Москва'):
        params = self.params
        params.update({
            'hometown': hometown,
            'sex': sex,
            'age_from': age,
            'age_to': age
            })
        response = r.get(f'{self.base_url}users.search', params=params)
        return response.json()

    def get_profile_pics_list(self, user_id):
            params = self.params
            items = []
            params.update({'user_id': user_id, 'album_id': 'profile',
                           'extended': 1, 'photo_sizes': 1})
            response = r.get(f'{self.base_url}photos.get', params=params)
            items += response.json()['response']['items']
# Пока не понял, надо ли обрабатывать 'next_from' в ответе, этот кусок кода можно подключить
# если ВК будет обрезать присылаемый перечень фоток профиля.
            # if 'next_from' in response.json()['response'].keys() != '':
            #     params.update({'start_from': 'next_from'})
            #     response = r.get(f'{self.base_url}photos.get', params=params)
            #     print(response.json())
            #     items += response.json()['response']['items']
            return sorted(items, key=lambda x: x['likes']['count'], reverse=True)[:3]

    def highest_resolution(self, photo):
        size_priority = ['w', 'z', 'y', 'r', 'q', 'p', 'o', 'x', 'm', 's']
        size_type = sorted([c['type'] for c in photo['sizes']],
                                key=lambda x: size_priority.index(x))
        return size_type[0]

    def download_photo(self, user_id):
        profile_pics_list = self.get_profile_pics_list(user_id)
        try:
            for photo in profile_pics_list:
                size_type = self.highest_resolution(photo)
                for elem in photo['sizes']:
                    if elem['type'] == size_type:
                        with open(f'{photo["id"]}.jpg', 'wb+') as f:
                            f.write(r.get(elem['url']).content)
        except:
            print('Программа завершена с ошибкой. Возможно отсутствует доступ к запрошенному профилю.')
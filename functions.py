import requests as r
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
            params.update({'user_id': user_id, 'album_id': 'profile',
                           'extended': 1, 'photo_sizes': 1, 'count': 3})
            response = r.get(f'{self.base_url}photos.get', params=params)
            return response.json()

    def highest_resolution(self, photo):
        size_priority = ['w', 'z', 'y', 'r', 'q', 'p', 'o', 'x', 'm', 's']
        size_type = sorted([c['type'] for c in photo['sizes']],
                                key=lambda x: size_priority.index(x))
        return size_type[0]

    def download_photo(self, user_id):
        response = self.get_profile_pics_list(user_id)
        try:
            for photo in response['response']['items']:
                size_type = self.highest_resolution(photo)
                for elem in photo['sizes']:
                    if elem['type'] == size_type:
                        r.get(elem['url'])
        except:
            print('Программа завершена с ошибкой. Возможно отсутствует доступ к запрошенному профилю.')
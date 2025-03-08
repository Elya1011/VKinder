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

    def get_city_id(self, city_name):
        params = self.params
        params.update({
            'q': city_name,
            'need_all': 0,
            'count': 1
            })
        response = r.get(f'{self.base_url}database.getCities', params=params)
        return response.json()['response']['items'][0]['id']

    def search_users(self, age=18, sex=0, city='Москва'):
        params = self.params
        params.update({
            'sort': 0,
            'count': 1000,
            'city_id': self.get_city_id(city),
            'sex': sex,
            'age_from': age,
            'age_to': age,
            'has_photo': 1,
            'fields': 'verified'
              })
        response = r.get(f'{self.base_url}users.search', params=params)
        search_result = [c for c in response.json()['response']['items'] if c['is_closed']==False]
        return search_result

    def get_profile_pics_list(self, user_id):
            params = self.params
            items = []
            params.update({'user_id': user_id, 'album_id': 'profile',
                           'extended': 1, 'photo_sizes': 1})
            response = r.get(f'{self.base_url}photos.get', params=params)
            items += response.json()['response']['items']
            filtered_bad_links = [item for item in items if item['sizes'] != []]
            return sorted(filtered_bad_links, key=lambda x: x['likes']['count'], reverse=True)[:3]


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

    def get_photo_links(self, user_id):
        profile_pics_list = self.get_profile_pics_list(user_id)
        links = []
        for photo in profile_pics_list:
            size_type = self.highest_resolution(photo)
            for elem in photo['sizes']:
                if elem['type'] == size_type:
                    links.append(elem['url'])
                    sleep(0.2)
        return links
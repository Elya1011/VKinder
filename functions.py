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
        local_params = self.params | \
        {
        'q': city_name,
        'need_all': 0,
        'count': 1
        }
        response = r.get(f'{self.base_url}database.getCities', params=local_params)
        return response.json()['response']['items'][0]['id']

    def search_users(self, age_from=18, age_to=18, sex=0, city='Москва'):
        local_params = self.params | \
        {
        'sort': 0,
        'count': 1000,
        'city_id': self.get_city_id(city),
        'sex': sex,
        'age_from': age_from,
        'age_to': age_to,
        'has_photo': 1,
        'fields': 'verified'
        }
        response = r.get(f'{self.base_url}users.search', params=local_params)
        search_result = [c for c in response.json()['response']['items'] if c['is_closed']==False]
        return search_result

    def get_profile_pics_list(self, user_id):
            params = self.params
            items = []
            params.update({'user_id': user_id,
                           'album_id': 'profile',
                           'extended': 1,
                           'photo_sizes': 1})
            response = r.get(f'{self.base_url}photos.get', params=params)
            print(response.json())
            items += response.json()['response']['items']
            filtered_bad_links = [item for item in items if item['sizes'] != []]
            print(sorted(filtered_bad_links, key=lambda x: x['likes']['count'], reverse=True)[:3])
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

    def save_search_result(self, search_request):
        search_result = self.search_users(**search_request)

        for profile in search_result:
            profile_id = profile['id']
            profile_name = f'{profile["first_name"]} {profile["last_name"]}'
            profile_link = f'https://vk.com/id{profile["id"]}'
            pics_list = self.get_photo_links(user_id=profile['id'])
            print(profile_id, profile_name, profile_link, pics_list)
            # adding_favorite_users(profile_id, profile_name, profile_link, pics_list[0])

            sleep(0.1)
            break
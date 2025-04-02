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

    def get_city_id(self, city_name) -> int:
        """Поиск id города для работы с API VK"""
        local_params = self.params | \
        {
        'q': city_name,
        'need_all': 0,
        'count': 1
        }
        response = r.get(f'{self.base_url}database.getCities', params=local_params)
        return response.json()['response']['items'][0]['id']

    def search_users(self, age_from=18, age_to=18, sex=0, city='Москва') -> list:
        """Возвращает список найденных результатов исключая закрытые страницы"""
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

    def get_profile_pics_list(self, user_id) -> list:
        """Возврат сортированных по наибольшему числу лайков фотографий - до 3х штук"""
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

    def get_photo_links(self, user_id) -> list:
        """Формирование списка адресов фотографий в формате для VK API"""
        profile_pics_list = self.get_profile_pics_list(user_id)
        links = []
        for photo in profile_pics_list:
            links.append(f"photo{photo['owner_id']}_{photo['id']}")
            sleep(0.2)
        print(links)
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
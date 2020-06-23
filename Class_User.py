import requests
import time

class User:
    def __init__(self, user_id, TOKEN):
        self.TOKEN = TOKEN
        if str(user_id).isdigit():
            self.USER_ID = user_id
        else:
            time.sleep(2)
            self.params = {
                'access_token': self.TOKEN,
                'v': 5.89,
                'screen_name': user_id
            }
            response = requests.get('https://api.vk.com/method/utils.resolveScreenName', params=self.params).json()
            self.USER_ID = response['response']['object_id']
        self.params = {
            'access_token': self.TOKEN,
            'v': 5.89,
            'user_id': self.USER_ID,
        }

    def get_groups(self):
        self.params['extended'] = 1
        self.params['fields'] = 'members_count'
        response = requests.get('https://api.vk.com/method/groups.get', params=self.params).json()
        return(response)

    def get_strip_groups_set(self):
        group_set = [item['id'] for item in User.get_groups(self)['response']['items']]
        return(group_set)

    def get_friends(self):
        response = requests.get('https://api.vk.com/method/friends.get', params=self.params).json()
        id_set = [item for item in response['response']['items']]
        return(id_set)
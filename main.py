import requests
import time
import json
from Class_User import User

TOKEN = 'a720aa36eb2a773251118006e41ae0b836bfbb63ef43790f3d63acc48cdf48544849e5b2039f220a74f1d'
user_id = input('Введите id пользователя: ')

def get_uncommon_groups(user_id):
    main_user = User(user_id, TOKEN)
    time.sleep(2)
    friend_set = main_user.get_friends()
    time.sleep(2)
    group_set = main_user.get_strip_groups_set()
    print('Проверяем друзей и их группы: ')
    counter = 1
    for friend_id in friend_set:
        user = User(friend_id, TOKEN)
        time.sleep(2)
        try:
            new_group_set = user.get_strip_groups_set()
        except KeyError:
            print(f'Невозможно проверить пользователя с id {friend_id}, поскольку его профиль приватный или был заблокирован')
            print(f'{counter}/{len(friend_set)}')
            counter += 1
            continue
        group_set = set(group_set) - set(new_group_set)
        print(f'{counter}/{len(friend_set)}')
        counter += 1
    return(group_set)

def get_data():
    data = []
    user = User(user_id, TOKEN)
    unique_groups = get_uncommon_groups(user_id)
    for group in user.get_groups()['response']['items']:
        if group['id'] in unique_groups:
            try:
                data.append({'name': group['name'], 'gid': group['id'], 'members_count': group['members_count']})
            except KeyError:
                continue
    return(data)

def dump_json():
    with open ('data.json', 'w', encoding='utf-8') as file:
        json.dump(get_data(), file, ensure_ascii=False)

dump_json()
import os
from InstagramAPI import InstagramAPI
from utils import get_list_from_csv
import pandas as pd

current_path = os.path.dirname(os.path.abspath(__file__))
file = open(current_path + '/../user.txt', 'r')
ids = [line[:-1] for line in file.readlines()]
name = ids[0]
pswd = ids[1]


def get_followings(data_file, username, password):
    # Get the user info
    user_full_name = get_list_from_csv(data_file, 0)
    user_name = get_list_from_csv(data_file, 1)
    user_id = get_list_from_csv(data_file, 2)

    all_friends_username = list()
    all_friends_full_name = list()
    all_friends_id = list()

    api = InstagramAPI(username, password)
    api.login()

    friends = api.getTotalFollowings(user_id[0])
    for friend in friends:
        all_friends_username.append(friend['username'])
        all_friends_full_name.append(friend['full_name'])
        all_friends_id.append(friend['pk'])

    user_name.extend(all_friends_username)
    user_full_name.extend(all_friends_full_name)
    user_id.extend(all_friends_id)

    user_network = [
        ('NAME', user_full_name),
        ('USERNAME', user_name),
        ('ID', user_id)]
    pd.DataFrame.from_items(user_network).to_csv(data_file, index=False)


if __name__ == '__main__':
    get_followings(current_path + '/../database/frotteman/player_username_id_team.csv',
                   name, pswd)

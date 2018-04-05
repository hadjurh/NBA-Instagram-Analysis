import os
from InstagramAPI import InstagramAPI
from utils import get_list_from_csv
import pandas as pd
from tqdm import tqdm


# File based
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


# Data frame based
def add_relationships(data_frame, username, password, relation='followings'):
    # Get the user info
    user_full_name = data_frame['NAME'].tolist()
    user_name = data_frame['USERNAME'].tolist()
    user_id = data_frame['ID'].tolist()
    user_private = data_frame['PRIVATE'].tolist()
    user_relation = ['Following']

    all_relations_username = list()
    all_relations_full_name = list()
    all_relations_id = list()
    all_relations_private = list()
    all_types_of_relation = list()

    api = InstagramAPI(username, password)
    api.login()

    followings = list()
    followers = list()
    if relation == 'followings':
        followings = api.getTotalFollowings(user_id[0])
    elif relation == 'followers':
        followers = api.getTotalFollowers(user_id[0])
    else:
        followings = api.getTotalFollowings(user_id[0])
        followers = api.getTotalFollowers(user_id[0])

    for user in followings:
        all_relations_username.append(user['username'])
        all_relations_full_name.append(user['full_name'])
        all_relations_id.append(user['pk'])
        all_relations_private.append(user['is_private'])
        all_types_of_relation.append('Following')

    for user in followers:
        all_relations_username.append(user['username'])
        all_relations_full_name.append(user['full_name'])
        all_relations_id.append(user['pk'])
        all_relations_private.append(user['is_private'])
        all_types_of_relation.append('Follower')

    user_name.extend(all_relations_username)
    user_full_name.extend(all_relations_full_name)
    user_id.extend(all_relations_id)
    user_private.extend(all_relations_private)
    user_relation.extend(all_types_of_relation)

    user_network = [
        ('NAME', user_full_name),
        ('USERNAME', user_name),
        ('ID', user_id),
        ('PRIVATE', user_private),
        ('RELATION', user_relation)]

    return pd.DataFrame.from_items(user_network)


if __name__ == '__main__':
    current_path = os.path.dirname(os.path.abspath(__file__))
    file = open(current_path + '/../user.txt', 'r')
    ids = [line[:-1] for line in file.readlines()]
    name = ids[0]
    pswd = ids[1]

    get_followings(current_path + '/../database/frotteman/player_username_id_team.csv',
                   name, pswd)

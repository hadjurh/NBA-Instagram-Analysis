from InstagramAPI import InstagramAPI
import json
import tqdm
from utils import get_list_from_csv


def get_insta_data(data_file, json_dest_file, username, password):
    # Get list of user names ['user_name1', 'user_name2', ...]
    user_names = get_list_from_csv(data_file, 1)

    # Get list of user IDs ['user_id1', 'user_id2', ...]
    user_ids = get_list_from_csv(data_file, 2)

    print('There are', len(user_names), "users to analyze (" + user_names[:3] + "...).")

    all_followings = dict.fromkeys(user_ids)

    api = InstagramAPI(username, password)
    api.login()

    i = 0
    for user_id in tqdm.tqdm(user_ids, unit='user'):
        friends = api.getTotalFollowings(user_id)
        followers_names = list()
        for friend in friends:
            followers_names.append(friend['username'])

        all_followings[user_id] = followers_names

        i += 1

    file = open(json_dest_file, 'w')
    json.dump(all_followings, file)


def get_insta_data_from_data_frame(data_frame, username, password):
    # Get list of user names ['user_name1', 'user_name2', ...]
    user_names = data_frame['USERNAME'].tolist()

    # Get list of user IDs ['user_id1', 'user_id2', ...]
    user_ids = data_frame['ID'].tolist()

    print('There are', len(user_names), "users to analyze (" + str(user_names[:3]) + "...).")

    all_followings = dict.fromkeys(user_names)

    api = InstagramAPI(username, password)
    api.login()

    i = 0
    for user_id, user_name in tqdm.tqdm(zip(user_ids, user_names), unit='user'):
        friends = api.getTotalFollowings(user_id)
        followers_names = list()
        for friend in friends:
            followers_names.append(friend['username'])

        all_followings[user_name] = followers_names

        i += 1

    return all_followings


if __name__ == '__main__':
    get_insta_data('../database/network_players_gt46_games/player_username_id_team.csv',
                   '../database/network_players_gt46_games/followings.json', '', '')

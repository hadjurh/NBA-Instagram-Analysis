import json
import numpy as np
import tqdm
from utils import get_list_from_csv


def build_dict(data_file, json_file):
    # Get list of user names ['user_name1', 'user_name2', ...]
    user_names = get_list_from_csv(data_file, 1)

    # Get list of user IDs ['user_id1', 'user_id2', ...]
    user_ids = get_list_from_csv(data_file, 2)

    all_followings = dict.fromkeys(user_names)

    ids_followings_file = json_file
    ids_followings_json = json.load(open(ids_followings_file))

    for user_id, user_name in zip(user_ids, user_names):
        all_followings[user_name] = ids_followings_json[user_id]

    return all_followings, user_ids, user_names


def build_adjacency_matrix(data_file, json_file):
    build = build_dict(data_file, json_file)
    ids_followings = build[0]
    user_names = build[2]

    adjacency_matrix = list()
    for user_name in tqdm.tqdm(user_names, unit='user'):
        followings = ids_followings[user_name]

        user_network = [int(user in followings) for user in user_names]

        adjacency_matrix.append(user_network)

    adjacency_matrix = np.matrix(adjacency_matrix)

    return adjacency_matrix


if __name__ == '__main__':
    network_matrix = build_adjacency_matrix('../database/network_players_gt46_games/player_username_id_team.csv',
                                            '../database/network_players_gt46_games/followings.json')
    np.savetxt("../database/network_players_gt46_games/adjacency_matrix.csv", network_matrix, delimiter=",", fmt='%.0i')

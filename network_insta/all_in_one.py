import os
import errno
import sys
import json
import time
import pandas as pd
import numpy as np
from optparse import OptionParser

from InstagramAPI import InstagramAPI
import tqdm

from get_user_info import add_attribute
from get_insta_data import get_insta_data_from_data_frame
from make_usercenter import add_relationships
from make_matrix_from_json_table import build_adjacency_matrix_data_frame


def setup_user(name, username, login, password):
    user_data_frame = pd.DataFrame([[name, username, False]], columns=['NAME', 'USERNAME', 'PRIVATE'])

    # Add ID to csv
    add_attribute(user_data_frame, 'ID')

    # Find relations ('followings', 'followers', or 'both')
    user_data_frame = add_relationships(user_data_frame, login, password, relation='followers')

    return user_data_frame


def setup_list_of_users(data_path, login, password):
    users_data_frame = pd.read_csv(data_path)
    users_names = users_data_frame['USERNAME'].tolist()

    # Add ID to csv
    api = InstagramAPI(login, password)
    api.login()

    users_username = list()
    users_full_name = list()
    users_id = list()
    users_private = list()
    users_media_count = list()
    users_follower_count = list()
    users_following_count = list()
    users_biography = list()

    for user in tqdm.tqdm(users_names):
        time.sleep(abs(np.random.normal(1, 0.2)))
        api.searchUsername(user)
        last_json = api.LastJson
        users_username.append(last_json['user']['username'])
        users_full_name.append(last_json['user']['full_name'])
        users_id.append(last_json['user']['pk'])
        users_private.append(last_json['user']['is_private'])
        users_media_count.append(last_json['user']['media_count'])
        users_follower_count.append(last_json['user']['follower_count'])
        users_following_count.append(last_json['user']['following_count'])
        users_biography.append(last_json['user']['biography'])

    users_list = [
        ('NAME', users_full_name),
        ('USERNAME', users_username),
        ('ID', users_id),
        ('PRIVATE', users_private),
        ('MEDIA_COUNT', users_media_count),
        ('FOLLOWERS', users_follower_count),
        ('FOLLOWING', users_following_count),
        ('MEDIA_COUNT', users_biography)]
    # TODO gerer les erreurs en memorisant a chaque iteration

    return pd.DataFrame.from_items(users_list)


def make_network(user_data_frame, folder_path, login, password, have_user_rights):
    # Create folder
    try:
        os.makedirs(folder_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    # Remove unreachable accounts
    if have_user_rights:
        user_data_frame = user_data_frame.loc[
            ~(user_data_frame['PRIVATE'] & (user_data_frame['RELATION'] == 'Follower'))]
    else:
        user_data_frame = user_data_frame.loc[~(user_data_frame['PRIVATE'])]
    # Get relations' followings
    relationship_dict = get_insta_data_from_data_frame(user_data_frame, login, password)

    # Create json file
    file = open(folder_path + '/relations.json', 'w')
    json.dump(relationship_dict, file)

    # Make adjacency matrix
    adjacency_matrix = build_adjacency_matrix_data_frame(user_data_frame, relationship_dict)

    # Write in files
    np.savetxt(folder_path + '/adjacency_matrix.csv', adjacency_matrix, delimiter=",", fmt='%.0i')
    user_data_frame.to_csv(folder_path + '/user_data_frame.csv', index=False)


if __name__ == '__main__':
    # Option parse
    parser = OptionParser()
    parser.add_option("--usercenter", dest="usercenter", action="store",
                      help="Center of the network's username", default='')
    parser.add_option("--users_file", dest="users_file", action="store",
                      help="CSV File containing all desired users", default='')
    parser.add_option("--fullname", dest="fullname", action="store",
                      help="Center of the network's full name", default='')
    parser.add_option("--idsfile", dest="idsfile", action="store",
                      help="File containing Instagram ids", default='')
    (options, args) = parser.parse_args()

    # Init path
    program_path = os.path.dirname(os.path.abspath(__file__))

    # Get IDs
    ids_file = open(program_path + '/../' + options.idsfile, 'r')
    ids_file = [line[:-1] for line in ids_file.readlines()]
    log = ids_file[0]
    pswd = ids_file[1]

    if len(options.usercenter) > 1:
        database_path = program_path + '/../database/network/' + options.usercenter
        user_rights = options.usercenter == log
        starting_data_frame = setup_user(options.fullname, options.usercenter, log, pswd)
    else:
        data_frame_path = program_path + '/../database/network/' + options.users_file
        user_rights = False
        starting_data_frame = setup_list_of_users(data_frame_path, log, pswd)
        print(starting_data_frame)

    # make_network(starting_data_frame, database_path, log, pswd, user_rights)

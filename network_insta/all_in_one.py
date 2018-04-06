import os
import errno
import sys
import json
import pandas as pd
import numpy as np
from optparse import OptionParser

from get_user_info import add_attribute
from get_insta_data import get_insta_data_from_data_frame
from make_usercenter import add_relationships
from make_matrix_from_json_table import build_adjacency_matrix_data_frame


def make_network(name, username, folder_path, login, password, have_user_rights):
    # Create folder and csv file (Name, Username)
    try:
        os.makedirs(folder_path)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    user_data_frame = pd.DataFrame([[name, username, False]], columns=['NAME', 'USERNAME', 'PRIVATE'])

    # Add ID to csv
    add_attribute(user_data_frame, 'ID')

    # Find relations ('followings', 'followers', or 'both')
    user_data_frame = add_relationships(user_data_frame, login, password, relation='followers')

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
                      help="Center of the network's username", default=False)
    parser.add_option("--users_file", dest="users_file", action="store",
                      help="CSV File containing all desired users", default=False)
    parser.add_option("--fullname", dest="fullname", action="store",
                      help="Center of the network's full name", default=False)
    parser.add_option("--idsfile", dest="idsfile", action="store",
                      help="File containing Instagram ids", default=False)
    (options, args) = parser.parse_args()

    # Init parameters
    program_path = os.path.dirname(os.path.abspath(__file__))
    database_path = program_path + '/../database/' + options.usercenter

    ids_file = open(program_path + '/../' + options.idsfile, 'r')
    ids_file = [line[:-1] for line in ids_file.readlines()]
    log = ids_file[0]
    pswd = ids_file[1]

    user_rights = options.usercenter == log

    make_network(options.fullname, options.usercenter, database_path, log, pswd, user_rights)

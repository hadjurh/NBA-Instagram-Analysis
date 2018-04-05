import os
import errno
import sys
import json
import pandas as pd
import numpy as np
from get_user_info import add_attribute
from get_insta_data import get_insta_data_from_data_frame
from make_usercenter import add_relationships
from make_matrix_from_json_table import build_adjacency_matrix_data_frame

name = 'Hugo'
username = 'frotteman'

current_path = os.path.dirname(os.path.abspath(__file__))
folder_path = current_path + '/../database/' + username

file = open(current_path + '/../' + sys.argv[1], 'r')
ids = [line[:-1] for line in file.readlines()]
login = ids[0]
password = ids[1]

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

# Remove unreachable accounts (private followers)
user_data_frame = user_data_frame.loc[~(user_data_frame['PRIVATE'] & (user_data_frame['RELATION'] == 'Follower'))]

# Get relations' followings
relationship_dict = get_insta_data_from_data_frame(user_data_frame, login, password)

# Create json file
file = open(folder_path + '/relations.json', 'w')
json.dump(relationship_dict, file)

# Make adjacency matrix
adjacency_matrix = build_adjacency_matrix_data_frame(user_data_frame, relationship_dict)
np.savetxt(folder_path + '/adjacency_matrix.csv', adjacency_matrix, delimiter=",", fmt='%.0i')

# Plot


user_data_frame.to_csv(folder_path + '/user_data_frame.csv', index=False)

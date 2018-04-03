import sys
import os
from optparse import OptionParser
import numpy as np
from get_insta_data import get_insta_data
from make_matrix_from_json_table import build_adjacency_matrix

# ARG1 Name of new folder where to put 'player_username_id_team.csv'
# ARG2 Folder that contains your username and password ("username\npassword\n")

# Option parse
# parser = OptionParser()
# parser.add_option("--usercenter", dest="usercenter", action="store",
#                   help="Center of the network", default=False)
# (options, args) = parser.parse_args()

current_path = os.path.dirname(os.path.abspath(__file__))

folder_path = current_path + '/../database/' + sys.argv[1]
players_data = folder_path + '/player_username_id_team.csv'
json_file = folder_path + '/followings.json'
matrix_file = folder_path + '/adjacency_matrix.csv'
pass_file = sys.argv[2]

file = open(pass_file, 'r')
ids = [line[:-1] for line in file.readlines()]
username = ids[0]
password = ids[1]


def main(argv):
    # if options.usercenter:
    #     print(options.usercenter)

    # Adjacency matrix build
    get_insta_data(players_data, json_file, username, password)
    network_matrix = build_adjacency_matrix(players_data, json_file)
    np.savetxt(matrix_file, network_matrix, delimiter=",", fmt='%.0i')


if __name__ == '__main__':
    main(argv=sys.argv)

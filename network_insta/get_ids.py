import requests
from utils import get_list_from_csv


def get_ids(data_file, dest_file):
    # Get list of user names ['user_name1', 'user_name2', ...]
    users = get_list_from_csv(data_file, 1)

    file = open(dest_file, 'w')

    # Go to specific user
    for user in users:
        print(user)
        url = 'https://www.instagram.com/' + user + '/?__a=1'
        data = requests.get(url=url)
        data = data.json()
        file.write(data['graphql']['user']['id'] + '\n')


if __name__ == '__main__':
    # Store IDs in 'ids.txt'.
    # Process it manually.
    get_ids('../database/player_username_team_2017-18.csv', '../database/ids.txt')

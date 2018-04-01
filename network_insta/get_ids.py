import requests
import csv


def get_ids(source_file_path, dest_file_path):
    # Get list of users ['user1', 'user2', ...]
    users = list()
    with open(source_file_path, newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            users.append(row[1])
    users = users[1:]  # Remove column name

    file = open(dest_file_path, 'w')

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

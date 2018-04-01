from InstagramAPI import InstagramAPI
import requests

# Get list of users ['user1', 'user2', ...]
file = open('../get_data_from_scraper/usernames.txt', 'r')
users = [line[:-1] for line in file.readlines()]
users = users[260:]

file = open('../get_data_from_scraper/ids2.txt', 'w')

# Go to specific user
for user in users:
    print(user)
    url = 'https://www.instagram.com/' + user + '/?__a=1'
    resp = requests.get(url=url)
    data = resp.json()

    file.write(data['graphql']['user']['id'] + '\n')
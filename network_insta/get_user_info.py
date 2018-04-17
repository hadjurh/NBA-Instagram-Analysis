import requests
import pandas as pd
from tqdm import tqdm
from utils import get_list_from_csv
from InstagramAPI import InstagramAPI


# File based
def get_attribute(data_file, attribute):
    # Get list of user names ['user_name1', 'user_name2', ...]
    players_data = pd.read_csv(data_file)

    user_names = players_data['USERNAME']
    length = len(user_names)

    if attribute in players_data.columns:
        to_add = [item for item in players_data[attribute] if item != 0]
        start = [item for item in players_data[attribute]].index(0)
    else:
        to_add = list()
        start = 0

    # Go to specific user
    for i in tqdm(range(start, length), unit='user'):
        url = 'https://www.instagram.com/' + user_names[i] + '/?__a=1'
        data = requests.get(url=url)
        data = data.json()

        value = int()
        if attribute == 'ID':
            value = data['graphql']['user']['id']
        elif attribute == 'FOLLOWERS':
            value = data['graphql']['user']['edge_followed_by']['count']

        to_add.append(value)

        players_data[attribute] = pd.Series(to_add + ([0] * (length - i - 1)))

        # Store updated data at each step to prevent crash (because Instagram limits requests number)
        players_data.to_csv(data_file, index=False)


# Data frame based
def add_attribute(data_frame, attribute, login, password):
    user_names = data_frame['USERNAME']
    length = len(user_names)

    api = InstagramAPI(login, password)
    api.login()

    to_add = list()
    for i in tqdm(range(length)):
        api.searchUsername(user_names[i])
        last_json = api.LastJson
        print(last_json)

        if attribute == 'ID':
            to_add.append(last_json['user']['pk'])
        elif attribute == 'FOLLOWERS':
            to_add.append(last_json['user']['followers_count'])

    # if attribute in data_frame.columns:
    #     to_add = [item for item in data_frame[attribute] if item != 0]
    #     start = [item for item in data_frame[attribute]].index(0)
    # else:
    #     to_add = list()
    #     start = 0

    # Go to specific user
    # for i in tqdm(range(start, length), unit='user'):
    #     url = 'https://www.instagram.com/' + user_names[i] + '/?__a=1'
    #     data = requests.get(url=url)
    #     data = data.json()
    #
    #     value = int()
    #     if attribute == 'ID':
    #         value = data['graphql']['user']['id']
    #     elif attribute == 'FOLLOWERS':
    #         value = data['graphql']['user']['edge_followed_by']['count']
    #
    #     to_add.append(value)

    data_frame[attribute] = pd.Series(to_add)


if __name__ == '__main__':
    df = pd.DataFrame([["Hugo", "frotteman", False]], columns=['NAME', 'USERNAME', 'PRIVATE'])
    add_attribute(df, 'ID', 'allstatsgame', 'Ichigaya38')
    print(df)

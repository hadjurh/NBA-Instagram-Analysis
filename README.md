# NBA Instagram Analysis :basketball: :camera: :bar_chart:

## Objectives

The goal of this project is to learn about NBA players activity on Instagram.
    
## Progress - Features

| Step          | Advancement   |
| ------------- | :-------------: |
| Manually search for active players username | &#10003; |
| Get each post stats (date, #likes, #comments, type of media) given a user | &#10003; |
| From a list of player, get the adjacency matrix of their relationships on Instagram | &#10003; |


## Usage & Options

* Store post by post stats in `database/instagram_user_by_user_data/username.txt`.

    Command: `python3 get_data_from_scraper/get_data_personal.py username1 username2 ...`

    | Options        | Features       |
    | -------------  | -------------  |
    | `--filename`   | Get the data for each user in the file |
    
* Build the adjacency matrix from a list of users. 
Make sure to create a folder in `database/` which contains `player_username_id_team.csv`.
This file must contain columns named `'USERNAME'` and `'ID'` 
where the usernames and IDs wanted are stored.
Make sure to also create a file `user.txt` which contains `'username \n password \n'`.

    Command: `python3 network_insta/build_network.py name_of_folder user.txt`
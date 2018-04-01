#### Requirements

`usernames.txt` filled with the users to include in the network.
These must be users that follow a reasonable amount of account (<<1,000,000).

#### Get ID

`python3 get_ids.py` and manually put `id2.txt` content in `id.txt` because requests are crashing.

#### Make the network 

Move `id.txt` content to `ids_private_removed.txt` and 
remove each (private) id that makes the program crash.
**Put `\n` at the end of both ids and user names files.**


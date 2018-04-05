import pandas as pd


# Get list from csv ['row_1_col_index', 'row_2_col_index', ...]
def get_list_from_csv(file_path, index, header=True):
    data_frame = pd.read_csv(file_path)
    return data_frame.iloc[:, index].tolist()


if __name__ == '__main__':
    get_list_from_csv('/Users/hugo.h/Documents/documents_hugo/Perso/NBA_Instagram_Analysis/database/frotteman/player_username_id_team.csv',
                      1)

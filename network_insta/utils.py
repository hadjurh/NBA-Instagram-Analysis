import csv


# Get list from csv ['row_1_col_index', 'row_2_col_index', ...]
def get_list_from_csv(file_path, index, header=True):
    list_from_csv = list()

    with open(file_path, newline='') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            list_from_csv.append(row[index])

    if header:
        list_from_csv = list_from_csv[1:]  # Remove column name

    return list_from_csv

import os
import pandas


def load_file_list(path):
    file_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file_list.append(file)
    return file_list


def load_csv(root, file):
    file = os.path.join(root, file)
    return pandas.read_csv(file, header=None).values.tolist()

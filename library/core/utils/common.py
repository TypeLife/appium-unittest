import os


def open_or_create(path, mode='r'):
    if os.path.isfile(path):
        os.remove(path)
    dir_name, file_name = os.path.split(path)
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)
    fp = open(path, mode)
    return fp

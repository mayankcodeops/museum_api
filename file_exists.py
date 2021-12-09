import os


def file_exists(path_to_file):
    """
    :param path_to_file: path to file which needs to be checked
    :return: True, if file exists
    """
    return os.path.exists(path_to_file)
import os
import logging


def generate_csv(directory, filename, df):
    """
    :param directory: directory where the CSV file needs to be written
    :param filename: name of the CSV file to be written.
    :param df: pandas dataframe
    """
    if not os.path.exists(directory):
        try:
            os.mkdir('reports')
        except OSError as ae:
            logging.exception("Something went wrong while creating the reports directory: {}".format(ae.args[-1]))

    df.to_csv(directory + filename, mode='w', index=False)
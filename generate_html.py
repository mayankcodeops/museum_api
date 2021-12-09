import os
import logging


def generate_html(directory, filename, df):
    """
    :param directory: directory where the html report needs to be generated.
    :param filename:  name of the HTML file to be generated
    :param df: pandas dataframe
    """
    if not os.path.exists(directory):
        try:
            os.mkdir('reports')
        except OSError as ae:
            logging.exception("Something went wrong while creating the reports directory: {}".format(ae.args[-1]))

    df.to_html(directory + filename)
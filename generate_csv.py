import os
import logging


class CSVConverter:
    """
    A class for generating CSV reports from JSON data

    Attributes
    ----------

    Methods
    -------
    generate_csv(self, directory, filename, df)
        Generates CSV report from JSON data
    """
    @staticmethod
    def convert(directory, filename, df):
        """
        This member function generates CSV reports from a pandas dataframe
        :param directory:
        :param filename:
        :param df:
        :return: None
        """
        if not os.path.exists(directory):
            try:
                os.mkdir('reports')
            except OSError as ae:
                logging.exception("Something went wrong while creating the reports directory: {}".format(ae.args[-1]))

        df.to_csv(directory + filename, mode='w', index=False)

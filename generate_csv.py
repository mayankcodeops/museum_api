import os
import logging


class CSVConverter:
    """
    A class for generating CSV reports from JSON data

    Attributes
    ----------
    directory: str
        the directory path for generating CSV reports
    filename: str
        name of the CSV report to be generated
    df: pandas dataframe object

    Methods
    -------
    generate_csv(self)
        Generates CSV report from JSON data
    """
    def __init__(self, directory, filename, df):
        self.df = df
        self.directory = directory
        self.filename = filename

    def generate_csv(self):
        """
        This static method generates CSV report
        :param self: class Instance
        """
        if not os.path.exists(self.directory):
            try:
                os.mkdir('reports')
            except OSError as ae:
                logging.exception("Something went wrong while creating the reports directory: {}".format(ae.args[-1]))

        self.df.to_csv(self.directory + self.filename, mode='w', index=False)
import os
import logging


class HTMLConverter:
    """
        A class for generating HTML reports from JSON data

        Attributes
        ----------
        directory: str
            the directory path for generating HTML reports
        filename: str
            name of the HTML report to be generated
        df: pandas dataframe object

        Methods
        -------
        generate_html(self)
            Generates CSV report from JSON data
        """
    def __init__(self, directory, filename, df):
        self.directory = directory
        self.filename = filename
        self.df = df

    def generate_html(self):
        if not os.path.exists(self.directory):
            try:
                os.mkdir('reports')
            except OSError as ae:
                logging.exception("Something went wrong while creating the reports directory: {}".format(ae.args[-1]))

        self.df.to_html(self.directory + self.filename)
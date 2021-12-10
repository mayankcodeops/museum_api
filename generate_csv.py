import os
import logging


class CSVConverter:
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
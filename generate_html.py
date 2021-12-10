import os
import logging


class HTMLConverter:
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
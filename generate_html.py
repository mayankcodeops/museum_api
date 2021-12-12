import os
import logging


class HTMLConverter:
    """
        A class for generating HTML reports from JSON data

        Attributes
        ----------

        Methods
        -------
        generate_html(self, directory, filename, df)
            Generates CSV report from JSON data
        """
    @staticmethod
    def convert(directory, filename, df):
        if not os.path.exists(directory):
            try:
                os.mkdir('reports')
            except OSError as ae:
                logging.exception("Something went wrong while creating the reports directory: {}".format(ae.args[-1]))

        df.to_html(directory + filename)

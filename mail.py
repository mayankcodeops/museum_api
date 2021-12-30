import os
import datetime
import smtplib
import ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
from jinja2 import Environment, PackageLoader, select_autoescape

from config import config

env = Environment(
    loader=PackageLoader("mail"),
    autoescape=select_autoescape()
)

logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.DEBUG)

CONFIG_NAME = os.environ.get('CONFIG_NAME', 'default')


def construct_message(sender, receiver, subject, body, file):
    """
    Constructes a MIMEMultipart message to send through SMTPLib
    :param sender: mail address of the sender or admin
    :param receiver: mail address of the receiver
    :param subject: subject of the mail to be sent
    :param body: html body of the mail, can be a template
    :param file: any attachment to be sent with mail
    :return: MIMEMultipart object
    """
    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = receiver
    message["Subject"] = subject

    message.attach(MIMEText(body, "html"))

    if file is not None:
        try:
            with open(file, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
        except OSError as err:
            logging.exception(f"Error while writing attachments to payload stream: {err.args[-1]}")

        encoders.encode_base64(part)

        part.add_header(
            "Content-Disposition",
            f"attachment; filename = {file}"
        )

        message.attach(part)
    return message


def send_mail(sender, receiver, subject, body, attachment=None):
    """
    Send mail using SMTPLib
    :param sender: mail address of the sender or admin
    :param receiver: mail address of the receiver
    :param subject: subject of the mail to be sent
    :param body: body of the mail,can be template
    :param attachment: attachment to be sent with the mail, default=None
    """
    message = construct_message(sender, receiver, subject, body, attachment)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as server:
        server.login(email, password)
        server.sendmail(sender, receiver, message.as_string())


if __name__ == '__main__':
    email = config[CONFIG_NAME].ADMIN_MAIL
    password = config[CONFIG_NAME].MAIL_PASSWD
    mail_subject = f'Museum API Reports - {datetime.datetime.now().strftime("%c")}'
    mail_template = env.get_template("report.html")
    mail_body = mail_template.render()
    send_mail(email, email, mail_subject, mail_body, "reports.zip")



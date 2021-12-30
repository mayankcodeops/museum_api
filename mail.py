import os
import datetime
import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
from config import config
from jinja2 import Environment, PackageLoader, select_autoescape
env = Environment(
    loader=PackageLoader("mail"),
    autoescape=select_autoescape()
)


CONFIG_NAME = os.environ.get('CONFIG_NAME', 'default')

logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.DEBUG)

mail_template = env.get_template("report.html")

email = config[CONFIG_NAME].ADMIN_MAIL
password = config[CONFIG_NAME].MAIL_PASSWD

from_address = email
to_address = email
subject = f'Museum API Reports - {datetime.datetime.now().strftime("%c")}'
body = mail_template.render()

message = MIMEMultipart()
message["From"] = from_address
message["To"] = to_address
message["Subject"] = subject

message.attach(MIMEText(body, "html"))

reports = "reports.zip"

try:
    with open(reports, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
except OSError as err:
    logging.exception(f"Error while writing attachments to payload stream: {err.args[-1]}")

encoders.encode_base64(part)

part.add_header(
    "Content-Disposition",
    f"attachment; filename = {reports}"
)

message.attach(part)
text = message.as_string()

context = ssl.create_default_context()

if __name__ == '__main__':
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(email, password)
        server.sendmail(from_address, to_address, text)


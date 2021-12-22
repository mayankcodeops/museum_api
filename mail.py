import smtplib
import getpass
import email
from config import config
import ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

email = "mayank.nimcet.188@gmail.com"
password = input("Password: ")

from_address = email
to_address = email
subject = "API Reports"
body = "Sending API Reports"

message = MIMEMultipart()
message["From"] = from_address
message["To"] = to_address
message["Subject"] = subject

message.attach(MIMEText(body, "plain"))

reports = "reports.zip"

with open(reports, "rb") as attachment:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

encoders.encode_base64(part)

part.add_header(
    "Content-Disposition",
    f"attachment; filename = {reports}"
)

message.attach(part)
text = message.as_string()

context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(email, password)
    server.sendmail(from_address, to_address, text)


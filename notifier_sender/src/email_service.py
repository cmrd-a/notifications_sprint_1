import smtplib
from dataclasses import dataclass
from email.message import EmailMessage

from config import settings


@dataclass
class EmailMessageParams:
    to: list[str]
    subject: str
    body: str


sender_user = settings.sender_email


class EmailService:
    def __init__(self):
        self.server = smtplib.SMTP_SSL(settings.smtp_host, settings.smtp_port)
        self.server.login(sender_user, settings.sender_password)

    def __del__(self):
        self.server.close()

    def send_message(self, params: EmailMessageParams):
        message = EmailMessage()
        message["From"] = sender_user
        message["To"] = ",".join(params.to)
        message["Subject"] = params.subject

        message.add_alternative(params.body, subtype="html")
        self.server.sendmail(sender_user, [sender_user], message.as_string())

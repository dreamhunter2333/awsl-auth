from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
from smtplib import SMTP
from urllib.parse import urlparse

from fastapi import HTTPException

from config import settings


from .base import MailClientBase


_logger = logging.getLogger(__name__)


class SmtpMailClient(MailClientBase):

    _type = "smtp"

    @classmethod
    def send_verify_code(cls, email: str, code: str) -> None:
        try:
            smtp_url_parts = urlparse(settings.smtp_url)
            with SMTP(smtp_url_parts.hostname, port=smtp_url_parts.port) as smtp:
                smtp.starttls()
                smtp.login(smtp_url_parts.username, smtp_url_parts.password)
                message = MIMEMultipart()
                message['From'] = smtp_url_parts.username
                message['To'] = email
                message['Subject'] = "AWSL Verify Code"
                message.attach(MIMEText(f"Your verify code is {code}", 'plain'))
                smtp.sendmail(smtp_url_parts.username, email, message.as_string())
                return
        except Exception as e:
            _logger.error(f"Failed to send verify code: {e}")
            raise HTTPException(
                status_code=400, detail=f"Failed to send verify code: {e}"
            )

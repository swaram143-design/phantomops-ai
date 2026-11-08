import os
import smtplib

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailTool:
    """SMTP delivery configured only through environment variables.

    Never commit SMTP credentials. The previous repository credential must be
    revoked at the provider because removing it from this file does not revoke it.
    """

    def __init__(self):
        self.email_address = os.getenv("SMTP_EMAIL", "").strip()
        self.password = os.getenv("SMTP_PASSWORD", "").strip()
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com").strip()
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))

    def configured(self):
        return bool(self.email_address and self.password)

    def send_email(self, recipient, subject, body, attachment_path=None):
        if not self.configured():
            return {
                "success": False,
                "error": "SMTP is not configured. Set SMTP_EMAIL and SMTP_PASSWORD.",
            }

        if not recipient or not str(recipient).strip():
            return {"success": False, "error": "A recipient email address is required."}

        msg = MIMEMultipart()
        msg["From"] = self.email_address
        msg["To"] = str(recipient).strip()
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain", "utf-8"))

        if attachment_path and os.path.isfile(attachment_path):
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                "attachment",
                filename=os.path.basename(attachment_path),
            )
            msg.attach(part)

        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=20) as server:
                server.starttls()
                server.login(self.email_address, self.password)
                server.sendmail(self.email_address, [str(recipient).strip()], msg.as_string())
            return {"success": True, "recipient": str(recipient).strip()}
        except Exception as error:
            return {"success": False, "error": str(error)}


email_tool = EmailTool()

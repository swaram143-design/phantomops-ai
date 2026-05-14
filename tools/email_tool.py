import smtplib
import os

from email.mime.text import (
    MIMEText
)

from email.mime.multipart import (
    MIMEMultipart
)

from email.mime.base import (
    MIMEBase
)

from email import encoders


class EmailTool:

    def __init__(self):

        self.email_address = (
            "phantomops.automation@gmail.com"
        )

        self.password = (
            "gvdt ngdp sbug kkjp"
        )

    def send_email(
        self,
        recipient,
        subject,
        body,
        attachment_path=None
    ):

        try:

            msg = (
                MIMEMultipart()
            )

            msg[
                "From"
            ] = self.email_address

            msg[
                "To"
            ] = recipient

            msg[
                "Subject"
            ] = subject

            msg.attach(
                MIMEText(
                    body,
                    "plain"
                )
            )

            if (

                attachment_path

                and

                os.path.exists(
                    attachment_path
                )

            ):

                with open(
                    attachment_path,
                    "rb"
                ) as attachment:

                    part = (
                        MIMEBase(
                            "application",
                            "octet-stream"
                        )
                    )

                    part.set_payload(
                        attachment.read()
                    )

                    encoders.encode_base64(
                        part
                    )

                    filename = (
                        os.path.basename(
                            attachment_path
                        )
                    )

                    part.add_header(
                        "Content-Disposition",
                        f"attachment; filename={filename}"
                    )

                    msg.attach(
                        part
                    )

            server = (
                smtplib.SMTP(
                    "smtp.gmail.com",
                    587
                )
            )

            server.starttls()

            server.login(
                self.email_address,
                self.password
            )

            server.sendmail(
                self.email_address,
                recipient,
                msg.as_string()
            )

            server.quit()

            print(
                f"[Email] Sent to "
                f"{recipient}"
            )

            return {

                "success": True,

                "recipient":
                    recipient
            }

        except Exception as error:

            return {

                "success": False,

                "error":
                    str(error)
            }


email_tool = (
    EmailTool()
)
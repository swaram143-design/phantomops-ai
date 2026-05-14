import smtplib

from email.mime.text import (
    MIMEText
)

from email.mime.multipart import (
    MIMEMultipart
)


class EmailEngine:

    def __init__(self):

        self.email = (
            "swaram143@gmail.com"
        )

        self.password = (
            "xksi yaov hreo hpbj"
        )

    def send_email(
        self,
        to_email,
        subject,
        body
    ):

        try:

            message = (
                MIMEMultipart()
            )

            message[
                "From"
            ] = self.email

            message[
                "To"
            ] = to_email

            message[
                "Subject"
            ] = subject

            message.attach(
                MIMEText(
                    body,
                    "plain"
                )
            )

            server = (
                smtplib.SMTP(
                    "smtp.gmail.com",
                    587
                )
            )

            server.starttls()

            server.login(
                self.email,
                self.password
            )

            server.sendmail(
                self.email,
                to_email,
                message.as_string()
            )

            server.quit()

            return {

                "success": True
            }

        except Exception as error:

            return {

                "success": False,

                "error":
                    str(error)
            }

    def generate_subject(
        self,
        project
    ):

        marketplace = (
            project.get(
                "marketplace",
                "Opportunity"
            )
        )

        return (
            f"AI Automation Proposal "
            f"for {marketplace}"
        )

    def generate_email_body(
        self,
        project
    ):

        proposal = (
            project.get(
                "generated_proposal",
                ""
            )
        )

        return f"""
Hello,

I recently reviewed your project opportunity and believe we can help significantly.

{proposal}

If you would like,
I would be happy to discuss implementation details and next steps.

Best regards,
PhantomOps AI
"""

    def send_project_proposal(
        self,
        project,
        email
    ):

        subject = (
            self.generate_subject(
                project
            )
        )

        body = (
            self.generate_email_body(
                project
            )
        )

        return self.send_email(
            email,
            subject,
            body
        )


email_engine = (
    EmailEngine()
)
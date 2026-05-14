import smtplib

from email.mime.text import MIMEText

from email.mime.multipart import MIMEMultipart

# =====================================================
# EMAIL CONFIG
# =====================================================

EMAIL_ADDRESS = "swaram143@gmail.com"

EMAIL_PASSWORD = "mtgu iysw rghk ppsb"

# =====================================================
# SEND EMAIL
# =====================================================

def send_email(

    recipient,
    subject,
    message
):

    try:

        # =============================================
        # CREATE EMAIL
        # =============================================

        msg = MIMEMultipart()

        msg["From"] = EMAIL_ADDRESS

        msg["To"] = recipient

        msg["Subject"] = subject

        msg.attach(

            MIMEText(
                message,
                "plain"
            )
        )

        # =============================================
        # CONNECT SMTP
        # =============================================

        server = smtplib.SMTP(

            "smtp.gmail.com",
            587
        )

        server.starttls()

        server.login(

            EMAIL_ADDRESS,
            EMAIL_PASSWORD
        )

        # =============================================
        # SEND
        # =============================================

        server.send_message(msg)

        server.quit()

        print(

            f"\nEmail sent to {recipient}"
        )

    except Exception as e:

        print(

            f"\nEmail Error: {e}"
        )
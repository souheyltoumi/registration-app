import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from enum import Enum
from dao.conf.model_settings import get_settings
from utils.common import CustomHTTPException
settings = get_settings()

"""
each enum value must be a str format function (not the call!) that takes the message parameters and returns the message str
"""
class MailTemplates(Enum):
    account_activation_token = """
            Hello,

            Thank you for signing up! Please find below the code to activate your account:
            {activation_code}
            (expiration in 1 minute)
            Best regards,
            Your RegistrationApp Team
            """.format
    account_refresh_token = """
            Hello,

            Please find below the new code to activate your account:
            {new_activation_code}
            (expiration in 1 minute)
            Best regards,
            Your RegistrationApp Team
            """.format
    account_activated_mail = """
            Hello,

            Your account is now active

            Best regards,
            Your RegistrationApp Team
            """

def send_mail(receiver_email, message_body, subject):
    # SMTP server configuration (for Gmail)
    smtp_server = settings.smtp.host
    port = settings.smtp.port

    sender_email = 'no-reply@registration-app.com'
    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    # Attach message body
    body = message_body
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Create a secure SSL context
        server = smtplib.SMTP(smtp_server, port)

        # Send email
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        raise CustomHTTPException(detail=f"[send_mail] error while sending email:{str(e)}", status_code=500)
    finally:
        server.quit()

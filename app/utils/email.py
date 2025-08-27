# utils/email_utils.py
import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

def send_email(to_email, subject, body):
    try:
        smtp_server = os.getenv('MAIL_SERVER')
        smtp_port = int(os.getenv('MAIL_PORT', 587))
        use_tls = os.getenv('MAIL_USE_TLS', 'True') == 'True'
        username = os.getenv('MAIL_USERNAME')
        password = os.getenv('MAIL_PASSWORD')
        sender = os.getenv('MAIL_DEFAULT_SENDER')

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = to_email

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            if use_tls:
                server.starttls()
            server.login(username, password)
            server.send_message(msg)

        print(f"[EMAIL SENT] To: {to_email}, Subject: {subject}")
    except Exception as e:
        print(f"[EMAIL FAILED] {e}")

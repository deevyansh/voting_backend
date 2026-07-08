import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

def send_otp_email(to_email, otp):
    sender = os.getenv("GMAIL_ADDRESS")
    password = os.getenv("GMAIL_APP_PASSWORD")

    message = MIMEText(f"Your OTP is: {otp}")
    message["Subject"] = "Your Voting App OTP"
    message["From"] = sender
    message["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, to_email, message.as_string())

if __name__ == "__main__":
    send_otp_email("devkhadria@gmail.com", "123456")
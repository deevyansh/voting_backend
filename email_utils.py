import os
from dotenv import load_dotenv

load_dotenv()

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_otp_email(to_email, otp):
    message = Mail(
        from_email=os.getenv("SENDER_EMAIL"),
        to_emails=to_email,
        subject="Your Voting App OTP",
        plain_text_content=f"Your OTP is: {otp}"
    )
    sg = SendGridAPIClient(os.getenv("SENDGRID_API_KEY"))
    try:
        response = sg.send(message)
        print("Status code:", response.status_code)
        print("Body:", response.body)
    except Exception as e:
        print("SendGrid error:", e)
        if hasattr(e, 'body'):
            print("Error body:", e.body)

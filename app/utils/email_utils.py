import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os


load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_otp_email(to_email: str, otp: str):
    print("to email: ", to_email, "otp: ", otp)
    msg = EmailMessage()
    msg["Subject"] = "Your OTP Verification Code"
    msg["From"] = EMAIL_USER
    msg["To"] = to_email
    msg.set_content(f"Your OTP is: {otp}\n\nPlease do not share it with anyone.")

    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_USER, EMAIL_PASSWORD)
            smtp.send_message(msg)
        return {"message": "OTP email sent successfully", "status": True }
    except Exception as e:
        print(f"error {e} ")
        return {"error": str(e)}


import os

from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

fernet_secret_key = os.getenv("FERNET_SECRET_KEY")

if not fernet_secret_key:
    raise ValueError("FERNET_SECRET_KEY not found in environment variables.")

fernet = Fernet(fernet_secret_key)

def incrept_email(email: str)-> str:
    encrypt_mail = fernet.encrypt(email.encode()).decode()
    
    return encrypt_mail  

def decrept_email(encryptEmail: str)->str:
    email = fernet.decrypt(encryptEmail.encode()).decode()
    
    return email
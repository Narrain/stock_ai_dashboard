# Handles SmartAPI authentication
import os
from dotenv import load_dotenv
from SmartApi import SmartConnect
import pyotp

load_dotenv()

def get_session():
    obj = SmartConnect(api_key=os.getenv("API_KEY"))
    totp = pyotp.TOTP(os.getenv("TOTP_SECRET")).now()
    session = obj.generateSession(os.getenv("CLIENT_CODE"), os.getenv("PASSWORD"), totp)
    return obj, session["data"]["jwtToken"]

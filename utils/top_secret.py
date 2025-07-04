import os
import pyotp
from dotenv import load_dotenv

load_dotenv()
totp = pyotp.TOTP(os.getenv("TOTP_SECRET"))
print("Login OTP:", totp.now())

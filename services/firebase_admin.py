import os
import firebase_admin
from firebase_admin import credentials
from dotenv import load_dotenv

load_dotenv()

def init_firebase_admin():
    """Initialize Firebase Admin once for the process."""
    if not firebase_admin._apps:
        cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "instance/firebase-admin.json")
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)

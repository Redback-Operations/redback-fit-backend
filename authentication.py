import pyrebase
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

config = {
    'apiKey': os.getenv("FIREBASE_API_KEY"),
    'authDomain': os.getenv("FIREBASE_AUTH_DOMAIN"),
    'projectId': os.getenv("FIREBASE_PROJECT_ID"),
    'storageBucket': os.getenv("FIREBASE_STORAGE_BUCKET"),
    'messagingSenderId': os.getenv("FIREBASE_MESSAGING_SENDER_ID"),
    'appId': os.getenv("FIREBASE_APP_ID"),
    'measurementId': os.getenv("FIREBASE_MEASUREMENT_ID"),
    'databaseURL': os.getenv("FIREBASE_DATABASE_URL")
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

email = 'test@gmail.com'
password = '123456'

# Uncomment to create a new user
# user = auth.create_user_with_email_and_password(email, password)
# print("User created:", user)

# Sign in existing user
user = auth.sign_in_with_email_and_password(email, password)
print("User signed in:", user)

# Uncomment to get account info
# info = auth.get_account_info(user['idToken'])
# print("Account info:", info)

# Uncomment to send password reset email
# auth.send_password_reset_email(email)

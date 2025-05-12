import pyrebase
from dotenv import load_dotenv
import os

# Load env variables
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

#Please adjust the environment variable to create a user, within the Flask database
email = os.getenv("TEST_EMAIL")
password = os.getenv("TEST_PASSWORD")

#user = auth.create_user_with_email_and_password(email, password)
#print(user)

user = auth.sign_in_with_email_and_password(email, password)

#info = auth.get_account_info(user['idToken'])
#print(info)

#auth.send_email_verification(user['idToken'])

#auth.send_password_reset_email(email)
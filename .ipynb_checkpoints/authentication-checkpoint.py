


import pyrebase

config = {
    'apiKey': "AIzaSyC7iwP0768QD5WWBdBVcAtwfSE1F7BSifw",
    'authDomain': "authenticatepy-40773.firebaseapp.com",
    'projectId': "authenticatepy-40773",
    'storageBucket': "authenticatepy-40773.appspot.com",
    'messagingSenderId': "161289377298",
    'appId': "1:161289377298:web:02259ecfacbe342798eacb",
    'measurementId': "G-Q2VBDEPT0V",
    'databaseURL': ''
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

email = 'test@gmail.com'
password ='123456'

#user = auth.create_user_with_email_and_password(email, password)
#print(user)

user = auth.sign_in_with_email_and_password(email,password)
#info =auth.get_account_info(user['idToken'])
#print(info)

#auth.send_email_verification(user['idToken'])

auth.send_password_reset_email(email)



import os
from dotenv import load_dotenv

# Locate and load .env (so os.environ is populated)
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

# import factory
from app import create_app

# Create the app 
app = create_app()

if __name__ == '__main__':
    host = app.config.get('HOST', '127.0.0.1')
    port = app.config.get('PORT', 5000)
    app.run(host=host, port=port)

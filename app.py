from flask import Flask, jsonify
from flask_cors import CORS
from api.routes import api
from api.profile import api as profile_api
from models.user import db, add_default_user
from dotenv import load_dotenv
import os

# Load from .env file
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(profile_api, url_prefix='/api/profile')

with app.app_context():
    db.create_all()
    add_default_user()

#Example API route
@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello from Flask!'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=int(os.getenv("PORT", 5000)))
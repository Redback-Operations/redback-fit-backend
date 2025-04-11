from flask import Flask, jsonify
from flask_cors import CORS
from api.routes import api  # Import the Blueprint
from models.user import init_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reflexion_pro.db'  #Database URI
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})  # Vite runs on 5173


# Set up the database within an app context
init_db(app)

# Register the API Blueprint
app.register_blueprint(api, url_prefix='/api')

@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello from Flask!'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
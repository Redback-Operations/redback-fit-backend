from flask import Flask, jsonify
from flask_cors import CORS
from api.routes import api  # Import the Blueprint

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})  # Vite runs on 5173

# Register the API Blueprint
app.register_blueprint(api, url_prefix='/api')

@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello from Flask!'}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
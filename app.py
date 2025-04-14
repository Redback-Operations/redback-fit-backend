from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from api.routes import api  # Import the Blueprint
import os

# Initialize Flask app
app = Flask(
    __name__,
    static_folder=os.path.join(os.getcwd(), "../redback-fit-web"),  # Move one level up and access redback-fit-web
    static_url_path="/"  # Serve files from the root URL
)

# Set up CORS for development purposes
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})  # Vite runs on port 5173

# Register the API Blueprint
app.register_blueprint(api, url_prefix='/api')

# Example API route
@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello from Flask!'}), 200

# Serve the frontend (index.html)
@app.route("/")
def home():
    try:
        return send_from_directory(app.static_folder, "index.html")
    except FileNotFoundError:
        return jsonify({"error": "index.html not found in the static folder"}), 404

if __name__ == '__main__':
    # Allow dynamic port configuration for flexibility
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
import os
from flask import Flask, request, render_template_string
from werkzeug.security import check_password_hash
import sqlite3

app = Flask(__name__)

# Load secret from environment
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-not-for-prod")

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()

    return "Logged in" if (row and check_password_hash(row[0], password)) else "Login failed"

def welcome():
    user_input = request.args.get('name', '')
    return render_template_string("<h1>Welcome " + user_input + "</h1>")

if __name__ == "__main__":
    app.run()

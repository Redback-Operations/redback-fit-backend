import os
import flask
from flask import Flask, request
import sqlite3

app = Flask(__name__)

# Hardcoded secret (should be flagged)
SECRET_KEY = "my_hardcoded_secret_key_12345"

# Vulnerable SQL query (should be flagged)
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    user = cursor.fetchone()
    return "Logged in" if user else "Login failed"

# XSS-like template rendering with unescaped input (should be flagged)
@app.route('/welcome')
def welcome():
    user_input = request.args.get('name')
    return flask.render_template_string("<h1>Welcome " + user_input + "</h1>")

# Debug mode enabled (should be flagged)
if __name__ == "__main__":
    app.run(debug=True)

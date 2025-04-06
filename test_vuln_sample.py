# test_vuln_sample.py

# Hardcoded secret
password = "admin123"

# SQL Injection pattern
def get_user(user_input):
    query = f"SELECT * FROM users WHERE id = {user_input}"
    cursor.execute(query)

# SSRF-like request
import requests
def fetch_url(user_url):
    return requests.get(user_url)

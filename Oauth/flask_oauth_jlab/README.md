# Flask OAuth Login Module

This module provides a simple, secure user authentication system using **Google OAuth 2.0**, built with Flask. It enables users to log in via their Google accounts and view their basic profile information.

This is designed to integrate into the Redback Fit backend project as a standalone authentication component.

---

#Features

- Google OAuth 2.0 login
- Session-based user authentication using Flask-Login
- Secure handling of user sessions (via cookies)
- CORS-enabled for frontend-backend integration
- Frontend built using plain HTML + JS (can be swapped out later)

#Usage

Visit the frontend in your browser.

Click “Login with Google”

You’ll be redirected to Google for authentication

On success, you’ll be returned to the frontend, and your email will be displayed

Click “Logout” to clear the session

#Dependencies

Flask

Flask-Dance

Flask-Login

Flask-CORS

oauthlib
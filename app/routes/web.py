from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from app.services.oauth_service import oauth  # or however you named your OAuth client

web_bp = Blueprint('web', __name__, template_folder='../../templates')

@web_bp.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        # your OAuth-or-form login logic here
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            # for example, if you’re using Firebase Admin custom tokens:
            user = oauth.provider.sign_in_with_email_and_password(email, password)
            session['user'] = email
            return redirect(url_for('web.home'))
        except Exception:
            error = "Login failed. Please check your credentials."
    return render_template('index.html', user=session.get('user'), error=error)

@web_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('web.index'))

@web_bp.route('/home')
def home():
    if 'user' in session:
        return render_template('home.html', user=session['user'])
    return redirect(url_for('web.index'))

@web_bp.route('/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello from Flask!'}), 200

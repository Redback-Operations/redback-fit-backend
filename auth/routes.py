from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required
from models import db, UserCredential, UserProfile
from app import limiter

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        name = request.form.get('name').strip()
        email = request.form.get('email').strip().lower()
        password = request.form.get('password')

        try: 
            if not name or not email or not password:
                raise ValueError("Name, email and password are required.")
            if UserCredential.query.filter_by(email=email).first():
                raise ValueError("Email already registered.")   
            
            # Create user credentials
            new_user = UserCredential(email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.flush()  # Ensure new_user.id is available

            
            profile = UserProfile(
                user_id=new_user.id,
                name=name,
                account=email,
                birthDate="---", #placeholder
                gender="---", #placeholder
            )
            db.session.add(profile)
            db.session.commit()


            login_user(new_user)
            return redirect(url_for("home"))
        
        except Exception as e:
            error = "Signup failed. "+ str(e)

    return render_template('signup.html', error=error)

@auth_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute") # Rate limiting to prevent brute-force attacks
def login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email').strip().lower()
        password = request.form.get('password')
        user = UserCredential.query.filter_by(email=email).first()
        remember = bool(request.form.get('remember'))

        if user and user.check_password(password):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            return redirect(next_page or url_for("home"))
        else:
            error = "Invalid email or password."

    return render_template('login.html', error=error)

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
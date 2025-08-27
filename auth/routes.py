from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required
from models import UserCredential, UserProfile
from urllib.parse import urlparse, urljoin
from extensions import db, limiter 
from sqlalchemy.exc import IntegrityError

auth_bp = Blueprint('auth', __name__, template_folder='templates')

def validate_password(pwd: str):
    if len(pwd) < 8:
        raise ValueError("Password must be at least 8 characters long.")
    if pwd.isdigit() or pwd.isalpha():
        raise ValueError("Password must contain both letters and numbers.")
    return True

def is_safe_url(target: str) -> bool:
    if not target:
        return False
    ref = urlparse(request.host_url)
    test = urlparse(urljoin(request.host_url, target))
    return test.scheme in ('http', 'https') and ref.netloc == test.netloc

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    if request.method == 'POST':
        name = request.form.get('name').strip()
        email = request.form.get('email').strip().lower()
        password = request.form.get('password')

        try: 
            # Validate inputs
            if not name or not email or not password:
                raise ValueError("Name, email and password are required.")
            validate_password(password)
            
            # Check if email already exists
            if UserCredential.query.filter_by(email=email).first():
                error = "signup failed. email already registered."
                return render_template('signup.html', error=error), 400  
            
            
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

            # Auto-login after signup
            login_user(new_user)
            return redirect(url_for("home"))
        
        except ValueError as e:
            db.session.rollback()
            error = "Signup failed. " + str(e) 
            return render_template('signup.html', error=error), 400
        
        except IntegrityError:
            db.session.rollback()
            error = "signup failed. email already registered."
            return render_template('signup.html', error=error), 400
        
        except Exception as e:
            db.session.rollback()
            error = "Signup failed. "+ str(e)
            return render_template('signup.html', error=error), 400

    return render_template('signup.html', error=error)

@auth_bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per minute", methods=['POST'], per_method=True) # Rate limiting to prevent brute-force attacks
def login():
    error = None
    if request.method == 'POST':
        email = request.form.get('email').strip().lower()
        password = request.form.get('password')
        next_page = request.args.get('next') or request.form.get('next')
        remember = bool(request.form.get('remember'))

        # Loopkup user
        user = UserCredential.query.filter_by(email=email).first()

        #Auth check
        if user and user.check_password(password):
            login_user(user, remember=remember)
            dest = next_page if is_safe_url(next_page) else url_for("home")
            return redirect(dest)
        else:
            return "Login failed. Incorrect email or password.", 400

    return render_template('login.html', error=None)

@auth_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


from flask import session, jsonify, request
from website.models.user_model import User
from website.utils.db import db
from website.view.view import homepage_search_redirect, password_reminder_alert, database_save_error_alert, welcome_user_login
from functools import wraps
from website.utils.config import Messages
import jwt 
from datetime import datetime, timedelta
# from app import ap

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return jsonify({'error': 'Unauthorized', 'redirect': '/login'}), 401
        return f(*args, **kwargs)
    return decorated_function

def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request/args.get('token');
        if not token:
            return jsonify({ 'error': 'Token missing.'})
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({ 'error': 'invalid token.'})
        
def add_user_to_db(user, email, password):
    """
    Adds user to the database.

    Args:
        user (str): The search query. No restrictions yet.
        email (int): The current page number. Optional, not functional yet.
        password (str): The name of the movie. 5-9 characters long no spaces and contain only alphanumeric characters.

    Returns:
        Response: Rendered template with the updated results.
    """
    session['username'] = user
    
    try:
        user_db = User(user, email, password)
        db.session.add(user_db)
        db.session.commit()

        password_reminder_alert(user, password) # routing alert // business logic
        return homepage_search_redirect()
    
    except Exception as e:
        db.session.rollback()
        database_save_error_alert(e)

    finally:
        close_session()


#CREATE JWT
def open_session(user):
    session['username'] = user
    session['loggged_in'] = True

    return Messages.welcome_back_user(user)
    # welcome_user_login(session['username'])

def create_jwt(user, welcome_message):
    print("This is the secret key:",app.config['SECRET_KEY'])
    token = jwt.encode({
        'user': user,
        'expiration': str(datetime.now() + timedelta(seconds=120))
    },
        app.config['SECRET_KEY'])
    return jsonify({ 'token': token.decode('utf-8')})

def close_session():
    session.pop('username', None)

def is_user_logged_in(session):
    return 'username' in session

def validate_credentials(username, password):
    """Helper function to validate username and password."""
    valid_user = User.validate_user(username)
    valid_password = User.validate_password(password)
    return valid_user, valid_password

def user_query_filter_by_name(user):
    found_user = User.query.filter_by(username=user).first() # modificar
    return found_user

def user_to_dict(user):
    return {
        "username": user.username,
        "id": user.id,
        "logged_in": True
        # Add more fields as needed
    }
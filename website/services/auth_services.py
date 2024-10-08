from flask import session, jsonify, request
from website.models.user_model import User
from website.utils.db import db
from website.view.view import homepage_search_redirect, password_reminder_alert, database_save_error_alert, welcome_user_login
from functools import wraps
from website.utils.settings import Messages
import jwt 
from datetime import datetime, timedelta, timezone
from decouple import config
# from app import ap

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return jsonify({'error': 'Unauthorized decorator', 'redirect': '/login'}), 401
        return f(*args, **kwargs)
    return decorated_function

class Security():
    secret = config('JWT_KEY')

    @classmethod
    def generate_token(cls, authenticated_user):
        payload = {
            "iat": datetime.now(timezone.utc),
            'exp': datetime.now(timezone.utc) + timedelta(minutes=10),
            'username': authenticated_user.username
        }
        return jwt.encode(payload, cls.secret, algorithm="HS256")
    
    @classmethod
    def verify_token(cls, headers):
        if 'Authorization' in headers.keys():
            authorization=headers['Authorization']
            jwt_payload = authorization.split(" ")[1]
            
            try:
                
                return jwt.decode(jwt_payload, cls.secret, algorithms=["HS256"])
            except (jwt.ExpiredSignatureError, jwt.InvalidIssuerError):
                print("Error: The token has expired")
        return False

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

def close_session():
    session.pop('username', None)

def is_user_logged_in(session):
    return 'username' in session

def validate_credentials(username, password):
    """Helper function to validate username and password."""
    validated_user = User.validate_user(username)
    validated_password = User.validate_password(password)
    return validated_user, validated_password

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
from flask import session
from website.models.user_model import User
from website.utils.db import db
from website.view.view import homepage_search_redirect, password_reminder_alert, database_save_error_alert, welcome_user_login

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

def open_session(user):
    session['username'] = user
    welcome_user_login(user)

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
from flask import Blueprint, request, session
from website.utils.db import db
from ..models.user_model import User
import re

auth = Blueprint("auth", __name__)

@auth.route('/', methods=['GET', 'POST'])
def index():
    from website.view import homepage_search_redirect, render_auth_template, already_loggedin_user

    if request.method == 'POST':
        return render_auth_template()

    else:
        if 'username' in session:
            already_loggedin_user(session["username"])
            return homepage_search_redirect()
        
        # print("No username in session!")
        return render_auth_template()
    
@auth.route('/login', methods=['GET', 'POST'])
def login():

    from website.view import homepage_search_redirect, logout_redirect, invalid_pass_registered_user, invalid_pass_new_user, redirect_login_auth, welcome_user_login

    if request.method == 'POST':

        session.permanent = True
        user, email, password = (request.form.get(data) for data in ['username', 'email', 'password'])
        password_check = r"^[A-Za-z0-9]{5,9}$"

        found_user = User.query.filter_by(username=user).first()


        if found_user: # If found in DB
            # print(f"user already in database.")
            session['username'] = user

            if re.match(password_check, password):

                if found_user.password == password:
                    welcome_user_login(user)
                    return homepage_search_redirect()

                else: # WHY DO I NEED THIS FOR?
                    print('missing password/email') # ?????
                    invalid_pass_registered_user()
                    return logout_redirect()

            else:
                invalid_pass_registered_user()
                return logout_redirect()

        else:
            check_password = re.match(password_check, password)

            if check_password:

                session['username'] = user

                add_user_to_db(user, email, password)
                
            else:
                # print('missing password/email')
                invalid_pass_new_user()
                return redirect_login_auth()

    return redirect_login_auth()

@auth.route('/logout')
def logout():

    from website.view import session_logout_warning, redirect_auth

    if 'username' in session:
        
        # remove the username from the session if it's there
        session_logout_warning(session['username'])
        close_session()
    
    return redirect_auth()

def add_user_to_db(user, email, password):

    from ..view import homepage_search_redirect, password_reminder_alert, database_error_alert

    try:

        user_db = User(user, email, password)
        db.session.add(user_db)
        db.session.commit()

        password_reminder_alert(user, password)
        return homepage_search_redirect()
    
    except Exception as e:
        db.session.rollback()
        database_error_alert(e)

    finally:
        close_session()

def close_session():
    session.pop('username', None)
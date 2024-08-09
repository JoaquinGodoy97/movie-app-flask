from flask import Blueprint, request, session
from website.models.user_model import User
from website.services.auth_services import add_user_to_db, close_session, open_session, is_user_logged_in, validate_credentials, user_query_filter_by_name
from website.view.view import (homepage_search_redirect, invalid_username, invalid_pass_registered_user, invalid_pass_new_user,
                            redirect_login_auth, render_auth_template, already_loggedin_user, session_logout_warning, login_redirect)

auth = Blueprint("auth", __name__)

@auth.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        return render_auth_template()

    else:
        if is_user_logged_in(session):
            already_loggedin_user(session["username"])
            return homepage_search_redirect()
        
        return render_auth_template()
    
@auth.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        session.permanent = True
        user, email, password = (request.form.get(data) for data in ['username', 'email', 'password'])

        found_user = user_query_filter_by_name(user)
        
        valid_user, valid_pass = validate_credentials(user, password)

        
        if found_user: # If found in DB
            if found_user.compare_password(password):
                open_session(user)
                return homepage_search_redirect()
                    
            else:
                invalid_pass_registered_user()
                return login_redirect()
        else:
            if not valid_user:
                invalid_username()
                return login_redirect()
            elif not valid_pass:
                invalid_pass_new_user()
                return login_redirect()
                
            else:
                add_user_to_db(user, email, password)

                return redirect_login_auth()

    return redirect_login_auth()

@auth.route('/logout')
def logout():
    if is_user_logged_in(session):
        session_logout_warning(session['username']) # Removes the username from the session if it's there
        close_session()
    
    return redirect_login_auth()
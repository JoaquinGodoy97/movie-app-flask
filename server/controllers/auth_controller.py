from flask import Blueprint, request, render_template, jsonify, send_from_directory, session
from server.services.auth_services import add_user_to_db, user_to_dict, open_session, close_session, validate_credentials, user_query_filter_by_name, login_required
from server.view.view import (user_already_loggedin, homepage_search_redirect_welcome_message, session_logout_success, has_valid_access, unauthorized_access_missing_token, homepage_search_redirect_new_user, invalid_pass_not_registered_user, invalid_token, invalid_format_auth, invalid_username_not_registered_user, invalid_username_registered_user, homepage_search_redirect, invalid_pass_registered_user,
                            redirect_login_auth)
from server.utils.settings import Messages
from server.services.auth_services import Security

auth = Blueprint("auth", __name__)

@auth.route('/', methods=['GET'])
def index():

    has_access = Security.verify_token(request.headers)
    if has_access:
        return has_valid_access(has_access['username'])
    
    return unauthorized_access_missing_token()

@auth.route('/login', methods=['POST'])
def login():

    # It's not necessary because of /@me but it helps to prevenet access
    has_access = Security.verify_token(request.headers)
    if has_access:
        return user_already_loggedin()

    session.permanent = True
    user, email, password = (request.json.get(data) for data in ['username', 'email', 'password'])

    print("user:", user, "password:", password)

    found_user = user_query_filter_by_name(user)
    validated_user, validated_password = validate_credentials(user, password)
    
    if found_user: # If found in DB
        if found_user.compare_password(password):
            open_session(found_user.username)
            encoded_token = Security.generate_token(found_user)
            return homepage_search_redirect_welcome_message(found_user.username, encoded_token)
        
        else:
            return invalid_username_registered_user()
        
    else:
        if not validated_user:
            if not validated_password:
                return invalid_format_auth()
            return invalid_username_not_registered_user()
        
        elif not validated_password:
            return invalid_pass_not_registered_user()
            
        else:
            add_user_to_db(user, email, password)
            found_user = user_query_filter_by_name(user)

            if found_user:
                token = Security.generate_token(found_user)
                return homepage_search_redirect_new_user(token=token)

            return redirect_login_auth()

@auth.route('/logout', methods=['POST'])
def logout():

    try:
        close_session()
        return session_logout_success()

    except Exception as e:
        print("Could not log out session:", e)

@auth.route('/@me')
def get_current_user():

    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return unauthorized_access_missing_token()

    user_data = Security.verify_token(request.headers)
    # If the token is invalid (user_data is False), return 401 Unauthorized
    if not user_data:
        return invalid_token()

    try:
        username = user_data.get('username')
        if username:
            print('sucess')
            return has_valid_access(username)
        else:
            return invalid_token()

    except Exception as e:
        print(f"Exception during token verification: {e}")  # Log any unexpected exceptions
        return unauthorized_access_missing_token()

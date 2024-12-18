from flask import Blueprint, request, session
from server.services.auth_services import Security, add_user_to_db, open_session, close_session, validate_credentials, user_query_filter_by_name
from server.view.view import (homepage_superadmin_redirect, user_already_loggedin, homepage_search_redirect_welcome_message, session_logout_success, has_valid_access, unauthorized_access_missing_token, homepage_search_redirect_new_user, invalid_pass_not_registered_user, invalid_token, invalid_format_auth, invalid_username_not_registered_user, invalid_username_registered_user, homepage_search_redirect, invalid_pass_registered_user,
                            redirect_login_auth)
from server.utils.settings import SUPER_ADMIN_USERNAME


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
    # user, email, password = (request.json.get(data) for data in ['username', 'email', 'password'])

    user = request.json.get("username", "").strip()
    email = request.json.get("email", "").strip()
    password = request.json.get("password", "").strip()

    found_user = user_query_filter_by_name(user)
    validated_user, validated_password = validate_credentials(user, password)
    
    if found_user: # If found in DB
        if found_user.compare_password(password):
            open_session(found_user.username)
            encoded_token = Security.generate_token(found_user)

            if found_user.username == SUPER_ADMIN_USERNAME:
                return homepage_superadmin_redirect(found_user.admin_status, encoded_token)
            
            return homepage_search_redirect_welcome_message(found_user.username, found_user.admin_status, found_user.id, encoded_token)
        
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

            try:
                add_user_to_db(user, password, email) # Email at the end because is optional CAREFUL
                found_user = user_query_filter_by_name(user)

                if found_user:
                    token = Security.generate_token(found_user)
                    return homepage_search_redirect_new_user(token=token)
            except Exception as e:
                print(e)

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

    # auth_header = request.headers.get('Authorization')
    # if not auth_header:
    #     return unauthorized_access_missing_token()

    user_data = Security.verify_token(request.headers)
    # If the token is invalid (user_data is False), return 401 Unauthorized
    if not user_data:
        return invalid_token()

    try:
        username = user_data.get('username')
        if username:
            return has_valid_access(username)
        else:
            return invalid_token()

    except Exception as e:
        print(f"Exception during token verification: {e}") 
        return unauthorized_access_missing_token()

@auth.route('/ping', methods=['GET'])
def ping():
    return "Server is active!", 200
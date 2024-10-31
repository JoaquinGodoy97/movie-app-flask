from flask import Blueprint, request, render_template, jsonify, send_from_directory, session
from server.services.auth_services import add_user_to_db, user_to_dict, open_session, is_user_logged_in, validate_credentials, user_query_filter_by_name, login_required
from server.view.view import (homepage_search_redirect, invalid_username, invalid_pass_registered_user, invalid_pass_new_user,
                            redirect_login_auth, render_auth_template, already_loggedin_user, session_logout_warning, login_redirect)
from server.utils.settings import Messages
from server.services.auth_services import Security

auth = Blueprint("auth", __name__)

@auth.route('/', methods=['GET'])
def index():

    has_access = Security.verify_token(request.headers)

    if has_access:
        return jsonify({'username': has_access['username'], "redirect": "/search" })
    
    return jsonify({"message": 'User not logged in'}), 401 

@auth.route('/login', methods=['POST'])
def login():

    has_access = Security.verify_token(request.headers)

    if has_access:
        return jsonify({ 'message': "User is logged in already.", "redirect": "/search" })

    session.permanent = True
    user, email, password = (request.json.get(data) for data in ['username', 'email', 'password'])

    found_user = user_query_filter_by_name(user)
    validated_user, validated_password = validate_credentials(user, password)
    
    if found_user: # If found in DB
        if found_user.compare_password(password):
            welcome_message = open_session(found_user.username)
            encoded_token = Security.generate_token(found_user)

            return homepage_search_redirect(encoded_token ,message=welcome_message)
        else:
            invalid_pass_registered_user()
            print('You introduced a wrong password')
            return render_auth_template(error_msg=Messages.ERROR_MSG_PASSINVALID)
    else:
        if not validated_user:
            invalid_username()
            print('Not the appropiate username')
            return login_redirect()
        elif not validated_password:
            invalid_pass_new_user()
            print('Not the appropiate password')
            return login_redirect()
            
        else:
            add_user_to_db(user, email, password)
            found_user = user_query_filter_by_name(user)

            if found_user:
                token = Security.generate_token(found_user)
                return homepage_search_redirect(token=token, message=Messages.USER_CREATED)

            return redirect_login_auth()

@auth.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return jsonify({'message': 'Logged out successfully', 'redirect': '/login'}), 200

@auth.route('/@me')
def get_current_user():

    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'Unauthorized'}), 401

    user_data = Security.verify_token(request.headers)
    # If the token is invalid (user_data is False), return 401 Unauthorized
    if not user_data:
        return jsonify({'error': 'Invalid or expired token', 'redirect': '/login'}), 401

    try:
        username = user_data.get('username')
        if username:
            print('sucess')
            return jsonify({'username': username})
        else:
            return jsonify({'error': 'Invalid token', 'redirect': '/login'}), 401

    except Exception as e:
        print(f"Exception during token verification: {e}")  # Log any unexpected exceptions
        return jsonify({'error': f'Unauthorized: {e}'}), 401
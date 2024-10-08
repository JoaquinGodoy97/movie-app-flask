from flask import Blueprint, request, render_template, jsonify, send_from_directory, session
from website.services.auth_services import add_user_to_db, user_to_dict, open_session, is_user_logged_in, validate_credentials, user_query_filter_by_name, login_required
from website.view.view import (homepage_search_redirect, invalid_username, invalid_pass_registered_user, invalid_pass_new_user,
                            redirect_login_auth, render_auth_template, already_loggedin_user, session_logout_warning, login_redirect)
from website.utils.settings import Messages
from website.services.auth_services import Security

auth = Blueprint("auth", __name__)

@auth.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return jsonify({'message': 'Auth template rendering is now handled by React'})
    else: 
        if is_user_logged_in(session):
            return homepage_search_redirect(Messages.MSG_USER_LOGGEDIN, session["username"])
            # return jsonify({'message': 'User already logged in', 'username': session["username"]})
        
        return jsonify({"message": 'User not logged in'})  # Corrected to use jsonify

@auth.route('/login', methods=['POST'])
def login():
    session.permanent = True
    user, email, password = (request.json.get(data) for data in ['username', 'email', 'password'])

    found_user = user_query_filter_by_name(user)
    validated_user, validated_password = validate_credentials(found_user.username, found_user.password)
    
    if found_user: # If found in DB
        if found_user.compare_password(password):
            welcome_message = open_session(found_user.username) # f"Welcome back {user}", "success" and open session['user']
            encoded_token = Security.generate_token(found_user)

            # print(user, password)
            # welcome_message = Messages.welcome_back_user(user)

            return homepage_search_redirect(encoded_token ,message=welcome_message)
        else:
            invalid_pass_registered_user()
            return render_auth_template(error_msg=Messages.ERROR_MSG_PASSINVALID)
            # return jsonify({'error': 'Invalid Password', 'redirect': '/login' }), 403
        
    else:
        if not validated_user:
            invalid_username()
            return login_redirect()
        elif not validated_password:
            invalid_pass_new_user()
            return login_redirect()
            
        else:
            add_user_to_db(user, email, password)
            return redirect_login_auth()

@auth.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return jsonify({'message': 'Logged out successfully', 'redirect': '/login'}), 200

@auth.route('/@me')
def get_current_user():

    user = session.get('username')

    if not user:
        session['logged_in'] = False
        return jsonify({"error": "Unauthorized", "logged_in": session['logged_in']}), 401
    
    user = user_query_filter_by_name(user)
    return jsonify(user_to_dict(user))
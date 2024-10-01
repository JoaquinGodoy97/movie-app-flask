from flask import Blueprint, request, render_template, jsonify, send_from_directory, session
from website.services.auth_services import add_user_to_db, close_session, open_session, is_user_logged_in, validate_credentials, user_query_filter_by_name
from website.view.view import (homepage_search_redirect, invalid_username, invalid_pass_registered_user, invalid_pass_new_user,
                            redirect_login_auth, render_auth_template, already_loggedin_user, session_logout_warning, login_redirect)
from website.utils.config import Messages


auth = Blueprint("auth", __name__)

@auth.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return jsonify({'message': 'Auth template rendering is now handled by React'})
    else: # GET
        if is_user_logged_in(session['username']):
            # already_loggedin_user(session["username"])
            return homepage_search_redirect(Messages.MSG_USER_LOGGEDIN, session["username"])
            # return jsonify({'message': 'User already logged in', 'username': session["username"]})
        
        return jsonify({"message": 'User not logged in'})  # Corrected to use jsonify

@auth.route('/login', methods=['POST'])
def login():
    session.permanent = True
    user, email, password = (request.json.get(data) for data in ['username', 'email', 'password'])
    print("User received from postman:", user)

    found_user = user_query_filter_by_name(user)
    
    valid_user, valid_pass = validate_credentials(user, password)
    
    if found_user: # If found in DB
        if found_user.compare_password(password):
            open_session(user) # f"Welcome back {user}", "success"
            print(user, password)
            session['username'] = user
            welcome_message = Messages.welcome_back_user(session['username'])

            return homepage_search_redirect(welcome_message, session['username'])
        else:
            invalid_pass_registered_user()
            return render_auth_template(error_msg=Messages.ERROR_MSG_PASSINVALID)
            # return jsonify({'error': 'Invalid Password', 'redirect': '/login' }), 403
        
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

# @auth.route('/check_session')
# def check_session():
#     if 'username' in session:   
#         return jsonify({'logged_in': True, 'username': session['username']}), 200
#     else:
#         return jsonify({'logged_in': False}), 401

@auth.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return jsonify({'message': 'Logged out successfully', 'redirect': '/login'}), 200

# @auth.errorhandler(404)
# def page_not_found(e):
#     logging.error(f"Page not found: {e}, route: {request.url}")
#     return render_template('404.html'), 404

@auth.route('/@me')
def get_current_user():

    from website.services.auth_services import user_to_dict

    user = session.get('username')

    # print("This is session /@me: ", user, session)

    if not user:
        return jsonify({"error": "Unauthorised"}), 401
    
    user = user_query_filter_by_name(user)

    return jsonify(user_to_dict(user))
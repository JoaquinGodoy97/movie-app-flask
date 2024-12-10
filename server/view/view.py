from flask import render_template, flash, redirect, jsonify, url_for, session
from server.utils.settings import Messages

# Display movies in their respective page

def display_movies(results, render_success, render_error): # for the moment keep user optional
    if results:
        movie_set = results['movie_set']
        total_pages = results['total_pages']
        # current_page = results['current_page']
        # search_result = results['search_result']
        # current_user = session['username']

        return jsonify({ "results": movie_set, "total_pages": total_pages, "redirect": render_success })
        # return render_template(template_success, movies=movie_set, search_result=search_result, current_page=current_page, total_pages=total_pages)
    else:
        return page_not_found()
    
def display_current_results(search_result, current_page):
    return jsonify({ "search_result": search_result, "current_page": current_page})

# RENDER TEMPLATES

# def render_auth_template():
#     return jsonify({"error": Messages.ERROR_MSG_PASSINVALID, "redirect": "/login"}), 401

def render_homepage_template():
    return render_template("index.html")

def render_wishlist_template():
    return render_template("wishlist.html")

def render_page_not_found():
    return render_template('404.html'), 404

# REDIRECTS

def redirect_login_auth():
    return jsonify({ "message": "Could not create user.", "redirect": "/login"})

def logout_redirect(message=""):
    return jsonify({ "message": message, "redirect": "/logout" })

def go_to_first_page_redirect(search_result, current_page, current_service): # 'results.results_search_list'
    # return redirect(url_for(current_service, search_result=search_result, current_page=current_page))
    return jsonify({ "redirect": f"/{current_service}/search?query={search_result}&page={current_page}", "current_page": 1, "search_result": search_result})

#-------

def wishlist_search_redirect(current_page, search_result):
    return redirect(url_for('wishlist.wishlist_search', current_page=current_page, search_result=search_result))

def wishlist_pages_redirect(current_page):
    return redirect(url_for('wishlist.wishlist_pages', current_page=current_page))

def results_pages_redirect(current_page, search_result):
    return redirect(url_for('results.results_search_list', search_result=search_result, current_page=current_page))




def homepage_search_redirect(token="", user_loggedin=None):
    return jsonify({ "redirect": "/search", 'token': token}), 200

def homepage_search_redirect_welcome_message(user, token="", user_loggedin=None):
    return jsonify({ 'message': Messages.welcome_back_user(user), "redirect": "/search", 'token': token}), 200

def homepage_search_redirect_new_user(token="", user_loggedin=None):
    return jsonify({ 'message': Messages.USER_CREATED, "redirect": "/search", 'token': token}), 200

def homepage_search_redirect_movies_not_found(token="", user_loggedin=None):
    return jsonify({ 'message': Messages.MOVIES_NOT_FOUND}), 404

def homepage_search_redirect_page_not_found(token="", user_loggedin=None):
    return jsonify({ 'message': Messages.PAGE_NOT_FOUND}), 404





def wishlist_redirect():
    return redirect(url_for('wishlist.wishlist_pages', current_page=1))


# FLASH DISPLAY ERRORS

"""PAGINATION"""

def page_not_found(user_loggedin=None):
    return jsonify({ 'message': Messages.PAGE_NOT_FOUND }), 404

def page_not_found_wishlist_warning():
    return flash("No movie with that name found in your Wishlist.", "warning")

def page_not_found_with_error(e):
    return flash(f"Page not found:{e}", "warning")

def page_not_found_with_error_in_page(page, e):
    return flash(f"Page number {page} not found: {e}", "warning")

def first_page_warning(search_result):
    return flash('Right now you are on the first page of ' + "\"" + search_result + "\" results.", 'warning')

def last_page_warning():
    return flash('You have reached the last page. Please go back if you want to look for more results.', 'warning')


"""TOKEN"""
def invalid_token():
    return jsonify({'message': 'Session Expired.', 'redirect': '/login', "error": "Invalid token."}), 440

def unauthorized_access_missing_token():
    return jsonify({'message': 'Unauthorized', 'redirect': '/login'}), 401

def has_valid_access(username):
    return jsonify({'username': username, 'redirect': '/search'}), 200

"""LOGOUT"""

def session_logout_success():
    return jsonify({'message': 'Logged out successfully', 'redirect': '/login'}), 200

"""LOGIN"""

def invalid_username_registered_user():
    return jsonify({ "message": Messages.ERROR_MSG_INVALIDPASSWORD, "redirect": "/login" }), 401

def invalid_pass_registered_user():
    return jsonify({"message": Messages.ERROR_MSG_PASSINVALID, "redirect": "/login"}), 401

def invalid_username_not_registered_user():
    return jsonify({"message": Messages.ERROR_MSG_INVALIDUSERNAME_NOTREGISTERED, "redirect": "/login"}), 401

def invalid_pass_not_registered_user():
    return jsonify({"message": Messages.ERROR_MSG_INVALIDPASS_NOTREGISTERED, "redirect": "/login"}), 401

def invalid_format_auth():
    return jsonify({"message": Messages.ERROR_MSG_AUTHINVALIDFORMAT, "redirect": "/login"}), 401

def user_already_loggedin():
    return jsonify({"message": Messages.MSG_USER_LOGGEDIN, "redurect": "/search"}), 401


"""DATA BASE"""

def database_save_error_alert(error):
    return flash(f"An error occurred while saving to the database: {str(error)}", "danger")

def database_delete_error_alert(error):
    return flash(f"An error occurred while deleting to the database: {str(error)}", "danger")

"""RESULTS"""

def alert_movie_already_added(movie_name, movie_id):
    return flash(f"Cannot add {movie_name, movie_id } to the Wishlist. Already added.", 'danger')

def alert_movie_successly_added(movie_name, movie_id):
    return flash(f"Added {movie_name, movie_id } to the Wishlist. Also this is the length of object movies.", 'success')

def alert_no_movie_added():
    return flash("No movies added.", "warning")


"""WISHLIST"""
def movie_already_added():
    return jsonify({ "message": "Movie already added."}), 409

def wrong_movie_request():
    return jsonify ({ "message": "Could not process the movie request."}), 400

def movies_limit_reached_database():
    return jsonify({ "message": "Limit reached. 50 Movies per user. Server in development." }), 403

def movie_added_success(user, movie_name):
    return jsonify({ "message": f"{user} you added {movie_name} to your Wishlist!", 'method': 'add'}), 200

def movie_removed_success():
    return jsonify({ "message": "Movie removed successfuly", "method": 'remove'}), 200

def get_movies_status(statuses):
    return jsonify({'statuses': statuses}), 200

def alert_no_movie_added_wishlist():
    return flash("No movies added to your Wishlist.", "warning")

def first_page_warning_wishlist():
    return flash('Right now you are on the first page of your Wishlist results.', 'warning')

"""WISHLIST.DATABASE"""

def database_wishlist_delete_erorr_alert(movie_name, movie_id):
    return flash(f"Removed {movie_name, movie_id} from the Wishlist.", 'danger')

def database_wishlist_save_success_alert(movie_name, movie_id):
    return flash(f"Added {movie_name, movie_id} to the Wishlist.", 'success')


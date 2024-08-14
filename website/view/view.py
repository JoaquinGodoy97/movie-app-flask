from flask import render_template, flash, redirect, url_for

# Display movies in their respective page

def display_movies(results, template_success, template_error):
    if results:
        movie_set = results['movie_set']
        total_pages = results['total_pages']
        current_page = results['current_page']
        search_result = results['search_result']

        return render_template(template_success, movies=movie_set, search_result=search_result, current_page=current_page, total_pages=total_pages)
    else:
        page_not_found_warning()
        return render_template(template_error)
    
def display_current_results(search_result, current_page):
    return redirect(url_for("results.results_search_list", search_result=search_result, current_page=current_page))

# RENDER TEMPLATES

def render_auth_template():
    return render_template("auth.html")

def render_homepage_template():
    return render_template("index.html")

def render_wishlist_template():
    return render_template("wishlist.html")

def render_page_not_found():
    return render_template('404.html'), 404

# REDIRECTS

def redirect_login_auth():
    return redirect(url_for("auth.index"))

def login_redirect():
    return redirect(url_for('auth.login'))

def logout_redirect():
    return redirect(url_for('auth.logout'))

def go_to_first_page_redirect(search_result, current_page, current_service): # 'results.results_search_list'
    return redirect(url_for(current_service, search_result=search_result, current_page=current_page))

# def go_to_default_page(search_result, current_page, current_service): # 'results.results_search_list'
#     return redirect(url_for(current_service, search_result=search_result, current_page=current_page))

# def go_to_page_in_service(search_result, current_page, current_service):
#     return redirect(url_for(current_service, search_result=search_result, current_page=current_page))

#--------

def go_to_next_page(search_result, current_page, current_service):
    return redirect(url_for(current_service, search_result=search_result, current_page=current_page))

def go_to_prev_page(search_result, current_page, current_service):
    return redirect(url_for(current_service, search_result=search_result, current_page=current_page))

#--------

# def go_to_next_page_wishlist(search_result, current_page, current_service):
#     return redirect(url_for(current_service, search_result=search_result, current_page=current_page))

# def go_to_prev_page_wishlist(search_result, current_page, current_service):
#     return redirect(url_for(current_service, search_result=search_result, current_page=current_page))

#-------

def wishlist_search_redirect(current_page, search_result):
    return redirect(url_for('wishlist.wishlist_search', current_page=current_page, search_result=search_result))

def wishlist_pages_redirect(current_page):
    return redirect(url_for('wishlist.wishlist_pages', current_page=current_page))

def results_pages_redirect(current_page, search_result):
    return redirect(url_for('results.results_search_list', current_page=current_page, search_result=search_result))

def homepage_search_redirect():
    return redirect(url_for("homepage.search"))

def wishlist_redirect():
    return redirect(url_for('wishlist.wishlist_pages', current_page=1))


# FLASH DISPLAY ERRORS

"""PAGINATION"""
def page_not_found_warning():
    return flash("Page not found.", "warning")

def page_not_found_with_error(e):
    return flash(f"Page not found:{e}", "warning")

def page_not_found_with_error_in_page(page, e):
    return flash(f"Page number {page} not found: {e}", "warning")

def first_page_warning(search_result):
    return flash('Right now you are on the first page of ' + "\"" + search_result + "\" results.", 'warning')

def last_page_warning():
    return flash('You have reached the last page. Please go back if you want to look for more results.', 'warning')

"""LOGIN"""

def session_logout_warning(session_username):
    return flash(f"{session_username} has been logged out", "dark")

def insert_valid_pass():
    return flash("Please insert a valid password", "danger")

def welcome_user_login(user):
    return flash(f"Welcome back {user}", "success")

def already_loggedin_user(user_session):
    return flash(f'Logged in as {user_session}', 'success')

def invalid_pass_new_user():
    return flash("If you are new insert a invalid password. Write a password between 5-9 characters long no spaces.", "warning")

def invalid_pass_registered_user():
    return flash(f"Invalid Password. Write a password between 5-9 characters long no spaces.", "danger")

def invalid_username():
    return flash(f"Invalid Username. Write a Username between 5-9 characters long no spaces.", "danger")

def password_reminder_alert(user, password): # New user
    return flash(f"You've logged in as {user}. Please don't forget your password is {password}", "success")

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

def alert_no_movie_added_wishlist():
    return flash("No movies added to your Wishlist.", "warning")

"""WISHLIST.DATABASE"""

def database_wishlist_delete_erorr_alert(movie_name, movie_id):
    return flash(f"Removed {movie_name, movie_id} from the Wishlist.", 'danger')

def database_wishlist_save_success_alert(movie_name, movie_id):
    return flash(f"Added {movie_name, movie_id} to the Wishlist.", 'success')


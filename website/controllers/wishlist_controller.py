from flask import Blueprint, render_template, request, url_for, redirect, session
from .results_controller import handle_form, get_set_of_movies
from website.models.wishlist_user_model import Wishlist_user
from website.utils.db import db
from website.config import BASE_URL, API_KEY
from website.view.view import (session_logout_warning, logout_redirect, display_movies, wishlist_redirect, 
                    alert_no_movie_added_wishlist, alert_movie_already_added, render_wishlist_template,
                    database_wishlist_save_success_alert, display_current_results)
from website.services.auth_services import is_user_logged_in
from website.services.wishlist_services import (get_results_by_movie_id, add_to_wishlist_db, remove_from_wishlist_db,
                                                filter_by_usersession_and_movieid, filter_by_usersession)

wishlist = Blueprint('wishlist', __name__)

@wishlist.route('/wishlist', methods=["POST", "GET"])
def wishlist_homepage(current_page = 1):
    return redirect(url_for('wishlist.wishlist_pages', current_page=current_page))

@wishlist.route('/wishlist/<int:current_page>', methods=["POST", "GET"])
def wishlist_pages(current_page):

    if is_user_logged_in(session) == False:
        return logout_redirect()

    results = filter_by_usersession(session['username'])

    if not results:
        alert_no_movie_added_wishlist()
        return render_wishlist_template()
    
    results = get_results_by_movie_id(results)

    # search_result = query_search()
    current_service = 'wishlist'
    search_result = ""
    movie_results = get_set_of_movies(results, current_page, search_result, current_service)

    # Filters pages out of range & returns to the main Wishlist page
    if current_page > movie_results['total_pages']:
        return wishlist_redirect()

    if request.method == 'POST':
        response = handle_form(movie_results)

        if response:
            return response

        #LOG OUT
        if request.form.get('logout') == 'Log Out':
            session_logout_warning(session['username'])
            return logout_redirect()
        
    return display_movies(movie_results, template_success='wishlist.html', template_error='wishlist.html')

@wishlist.route('/wishlist/<search_result>/<int:current_page>/<int:movie_id>/<movie_name>', methods=["POST", "GET"])
def add_to_wishlist(search_result, current_page, movie_name, movie_id):
    """
    Adds a movie to the user's wishlist if it doesn't already exist.

    Args:
        search_result (str): The search query.
        current_page (int): The current page number.
        movie_name (str): The name of the movie.
        movie_id (int): The ID of the movie.

    Returns:
        Response: Rendered template with the updated results.
    """
    
    if is_user_logged_in(session) == False:
        return logout_redirect()

    movie_exists = filter_by_usersession_and_movieid(session['username'], movie_id)

    if movie_exists:
        alert_movie_already_added(movie_name, movie_id)
    else:
        database_wishlist_save_success_alert(movie_name, movie_id)
        add_to_wishlist_db(movie_id, movie_name, user_id=session['username'])
        
    return display_current_results(search_result, current_page)

@wishlist.route('/wishlist/<int:current_page>/<int:movie_id>', methods=["POST", "GET"])
def remove_from_wishlist(current_page, movie_id):
    """
    Removes a movie from the user's wishlist.

    Args:
        search_result (str): The search query.
        current_page (int): The current page number.
        movie_name (str): The name of the movie.
        movie_id (int): The ID of the movie.

    Returns:
        Response: Rendered template with the updated results.
    """
    found_movie_to_delete = Wishlist_user.query.filter_by(mv_id=str(movie_id)).first()
    
    if found_movie_to_delete:
        remove_from_wishlist_db(found_movie_to_delete)

    return redirect(url_for("wishlist.wishlist_pages", current_page=current_page))

@wishlist.route('/wishlist/<search_result>/<int:current_page>', methods=["POST", "GET"])
def wishlist_search(search_result, current_page):

    from website.services.wishlist_services import filter_movies_by_search_if_any

    results = filter_by_usersession(session['username'])
    results = get_results_by_movie_id(results) # here it should be the filter
    print(search_result, 1)
    results = filter_movies_by_search_if_any(results, search_result) ######
    print(search_result, 2)
    movie_results = get_set_of_movies(results, current_page, search_result, current_service='wishlist')
    print(search_result, 3)
    print(movie_results['search_result'])
    print('this is wishlist endpoint with SEARCH')
    if request.method == 'POST':
        response = handle_form(movie_results)

        if response:
            return response

        #LOG OUT
        if request.form.get('logout') == 'Log Out':
            session_logout_warning(session['username'])
            return logout_redirect()
        
    return display_movies(movie_results, template_success='wishlist.html', template_error='wishlist.html')
    # return redirect(url_for("wishlist.wishlist_search", current_page=current_page, search_result=search_result))

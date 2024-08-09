from flask import session, Blueprint, request
from website.config import API_URL
from website.models.wishlist_user_model import Wishlist_user
from website.view.view import (alert_movie_already_added, display_current_results, database_wishlist_save_success_alert,
                        logout_redirect, display_movies, homepage_search_redirect, page_not_found)
from website.services.results_services import add_to_wishlist_db, fetch_movie_results, get_set_of_movies, fetch_multiple_pages, handle_form
from website.services.auth_services import is_user_logged_in

results = Blueprint('results', __name__)

@results.route('/results/<search_result>/<int:current_page>' , methods=["GET", "POST"])
def results_search_list(search_result, current_page):
    """
    Handles the search results display and pagination for movies.

    Args:
        search_result (str): The search query.
        current_page (int): The current page number.

    Returns:
        Response: Rendered template with search results or redirect.
    """
    if is_user_logged_in(session):
        logout_redirect()
    else:
        return 

    movie_results_no_page_separation = fetch_movie_results(search_result)

    # IF CURRENT PAGE IS NOT ITERABLE OBJECT and if it has objects
    if not movie_results_no_page_separation['results'] or current_page > movie_results_no_page_separation['total_pages']:
        page_not_found()
        return homepage_search_redirect()

    movies = fetch_multiple_pages(search_result, start_page=1, total_pages=movie_results_no_page_separation['total_pages'])

    movie_results = get_set_of_movies(movies, current_page, search_result, current_service='results')

    if request.method == 'POST':
        # breakpoint()
        
        response = handle_form(movie_results)
        if response:
            return response

    return display_movies(movie_results, template_success='results.html', template_error='index.html')

@results.route('/results/<search_result>/<int:current_page>/<movie_name>/<int:movie_id>' , methods=["GET", "POST"])
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
    # if It can be called from wishlist without affecting results would be ideal

    if is_user_logged_in(session) == False:
        return logout_redirect()

    #consultar_con_wishlist(user_id=session['username'], mv_id=movie_id, model) goes to wishlist service
    movie_exists = Wishlist_user.query.filter_by(user_id=session['username'], mv_id=movie_id).first()

    # check_wishlist_for_movie_match(user, movie_id)

    if movie_exists:
        alert_movie_already_added(movie_name, movie_id)
    else:
        database_wishlist_save_success_alert(movie_name, movie_id)
        add_to_wishlist_db(movie_id, movie_name, user_id=session['username'])
        
    return display_current_results(search_result, current_page)
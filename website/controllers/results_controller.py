from flask import session, Blueprint, request
from website.view.view import (logout_redirect, display_movies, homepage_search_redirect, page_not_found_warning)
from website.services.results_services import fetch_movie_results, get_set_of_movies, fetch_multiple_pages, handle_form
from website.services.auth_services import is_user_logged_in

results = Blueprint('results', __name__)

@results.route('/results' , methods=["GET", "POST"])
def send_to_homepage():
    return homepage_search_redirect()

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

    #  If current page out of range => not found or didn't receive an object
    if not movie_results_no_page_separation['results']:
        page_not_found_warning()
        return homepage_search_redirect()

    # Get all the items from all page no sepratation at all (by default)
    movies = fetch_multiple_pages(search_result, start_page=1, total_pages=movie_results_no_page_separation['total_pages'])

    # Set a separation => (set pages of 5 movies each)
    movie_results = get_set_of_movies(movies, current_page, search_result, current_service='results')

    
    if current_page > movie_results['total_pages']:
        page_not_found_warning()
        return homepage_search_redirect()
    
    if request.method == 'POST':
        response = handle_form(movie_results)

        if response:
            return response

    return display_movies(movie_results, template_success='results.html', template_error='index.html')

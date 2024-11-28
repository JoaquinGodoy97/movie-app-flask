from flask import session, Blueprint, request, jsonify
from server.view.view import (invalid_token, homepage_search_redirect, display_movies, homepage_search_redirect_movies_not_found, homepage_search_redirect_page_not_found)
from server.services.results_services import fetch_movie_results, get_set_of_movies, fetch_multiple_pages, handle_form
from server.services.auth_services import is_user_logged_in, Security
from server.utils.settings import Messages

results = Blueprint('results', __name__)

@results.route('/results' , methods=["GET"])
def send_to_homepage():
    return homepage_search_redirect()

@results.route('/results/search' , methods=["GET"])
def results_search_list():
    """
    Handles the search results display and pagination for movies.

    Args:
        search_result (str): The search query.
        current_page (int): The current page number.

    Returns:
        Response: Rendered template with search results or redirect.
    """

    has_access = Security.verify_token(request.headers)

    if has_access:
        
        search_result = request.args.get('query', '')
        current_page = request.args.get('page', 1, type=int)

        movie_results_no_page_separation = fetch_movie_results(search_result)
        
        if not movie_results_no_page_separation['results']:
            return homepage_search_redirect_movies_not_found()

        # Get all the items from all page no sepratation at all (by default)
        movies = fetch_multiple_pages(search_result, start_page=1, total_pages=movie_results_no_page_separation['total_pages'])

        # Set a separation => (set pages of 5 movies each)
        movie_results = get_set_of_movies(movies, current_page, search_result, current_service='results')
        
        if current_page > movie_results['total_pages']:
            return homepage_search_redirect_page_not_found()
        
        return display_movies(movie_results, render_success='/results', render_error='/search')
    else:
        return invalid_token()

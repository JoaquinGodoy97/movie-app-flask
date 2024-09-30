from flask import session, Blueprint, request
from website.view.view import (logout_redirect, display_movies, homepage_search_redirect, page_not_found_warning)
from website.services.results_services import fetch_movie_results, get_set_of_movies, fetch_multiple_pages, handle_form
from website.services.auth_services import is_user_logged_in

results = Blueprint('results', __name__)

@results.route('/results' , methods=["GET", "POST"])
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
    if not is_user_logged_in(session):
        message = "User not logged in"
        return logout_redirect(message=message)
    
    search_result = request.args.get('query', '')
    current_page = request.args.get('page', 1, type=int)

    movie_results_no_page_separation = fetch_movie_results(search_result)
    
    if not movie_results_no_page_separation['results']:
        error_msg = "No movies found"
        return homepage_search_redirect(message=error_msg)

    # Get all the items from all page no sepratation at all (by default)
    movies = fetch_multiple_pages(search_result, start_page=1, total_pages=movie_results_no_page_separation['total_pages'])

    # Set a separation => (set pages of 5 movies each)
    movie_results = get_set_of_movies(movies, current_page, search_result, current_service='results')
    
    if current_page > movie_results['total_pages']:
        error_msg = "Page not found"
        return homepage_search_redirect(message=error_msg)
    
    # if request.method == 'POST':
    #     response = handle_form(movie_results)

    #     if response:
    #         return response
    # return display_movies(movie_results)
    return display_movies(movie_results, render_success='/results', render_error='/search')

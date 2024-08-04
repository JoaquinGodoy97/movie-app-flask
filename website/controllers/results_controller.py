from flask import session, Blueprint, request
from website.config import API_URL
from website.models.wishlist_user_model import Wishlist_user
from website.models.movie_model import Movies
from website.controllers.wishlist_controller import add_to_wishlist_db
from website.view import (alert_movie_already_added, display_current_results, database_wishlist_save_success_alert,
                        logout_redirect, display_movies, homepage_search_redirect, page_not_found, page_not_found_with_error, 
                        first_page_warning, last_page_warning, go_to_next_page, go_to_prev_page, page_not_found_with_error_in_page)
from .search_controller import search
import requests

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
    if "username" not in session:
        return logout_redirect()

    movie_results_no_page_separation = fetch_movie_results(search_result)

    # IF CURRENT PAGE IS NOT ITERABLE OBJECT and if it has objects
    if not movie_results_no_page_separation['results'] or current_page > movie_results_no_page_separation['total_pages']:
        page_not_found()
        return homepage_search_redirect()

    movies = fetch_multiple_pages(search_result, start_page=1, total_pages=movie_results_no_page_separation['total_pages'])
    movie_results = get_set_of_movies(movies, current_page, search_result)

    if request.method == 'POST':
        
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

    if "username" not in session:
        return logout_redirect()

    movie_exists = Wishlist_user.query.filter_by(user_id=session['username'], mv_id=movie_id).first()

    if movie_exists:
        alert_movie_already_added(movie_name, movie_id)
    else:
        database_wishlist_save_success_alert(movie_name, movie_id)
        add_to_wishlist_db(movie_id, movie_name, user_id=session['username'])

    return display_current_results(search_result, current_page)

def fetch_movie_results(search_result):
    """
    Fetches movie results from the API.

    Returns:
        dict: JSON response containing movie results.
    """

    api_url_for_search_results = get_url(search_result)
    response = requests.get(api_url_for_search_results)
    
    """
    # Into a Dict Alternative
    # movies = json.loads(response.text) 
    global movies
    """

    return response.json()

def navigate_page(search_result, current_page, total_pages):
    """
    Handles navigation through pages for the movie search results.

    Returns:
        Response: Redirect to the next or previous page.
    """

    if request.form.get('npage') == 'Next':

        if current_page >= total_pages:
            last_page_warning()

        current_page += 1
        return go_to_next_page(search_result, current_page)

    elif request.form.get('ppage') == 'Prev':

        if current_page <= 1:
            first_page_warning(search_result)

        current_page -= 1
        return go_to_prev_page(search_result, current_page)
    
def handle_form(results):
    """
    Handles form submissions for logout, search, and pagination.

    Args:
        results (dict): Dictionary containing search results and pagination info.

    Returns:
        Response: Redirects a response based on form action.
    """
    logout_response = handle_logout()
    if logout_response:
        return logout_response

    search_response = handle_search()
    if search_response:
        return search_response

    # Handles pagination
    return navigate_page(results['search_result'], results['current_page'], results['total_pages'])

def get_url(search_result):
    if search_result:
        url = API_URL + "&query=" + search_result 

    else:
        url = API_URL + "&query=default"

    return url

def handle_search():
    """
    Handles the search form submission if any.

    Returns:
        Response: Redirect to search results or homepage.
    """

    search_text = request.form.get('search')

    if 'search' in request.form:
        if search_text != "":
            return search()
    else:
        return homepage_search_redirect()

def handle_logout():
    """
    Handles the logout form submission.
    """

    if request.form.get('logout') == 'Log Out':
            # session_logout_warning(session['username'])
            return logout_redirect()

def get_set_of_movies(movie_list, current_page, search_result):
    """
    Organizes a set of movies for display based on the current page.

    Returns:
        dict: Dictionary containing the movie set and pagination info.
    """
    movies = Movies(movie_list)

    try:
        return {
            "movie_set": movies.get_movies_by_page(current_page),
            "total_pages": movies.total_pages,
            "current_page": current_page,
            "search_result": search_result
        }
    except ValueError as e:
        page_not_found_with_error(e)
        return {
            "movie_set": [],
            "total_pages": movies.total_pages,
            "current_page": current_page,
            "search_result": search_result
        }

def fetch_multiple_pages(search_query, start_page, total_pages):
    """
    Fetches multiple pages of movie results from the API since it has more than 1 page (20 items per page),
    so I get them all in one variable.

    Returns:
        list: List of movies from all fetched pages.
    """
    all_movie_results = []

    for page in range(start_page, total_pages + 1):
        try:
            response = requests.get(API_URL + "&query=" + search_query + f"&page={page}")
            response.raise_for_status()  # Raise an exception for HTTP errors
            results_per_page = response.json()

            if 'results' in results_per_page:
                for movie in results_per_page['results']:

                    movie_data = {
                        'id': movie.get('id'),
                        'title': movie.get('title'),
                        'poster_path': movie.get('poster_path'),
                        'overview': movie.get('overview')
                    }

                    all_movie_results.append(movie_data)
                    
        except requests.exceptions.RequestException as e:
            page_not_found_with_error_in_page(page, e)
            continue

    return all_movie_results


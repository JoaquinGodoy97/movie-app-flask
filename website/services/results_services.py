from flask import request
from website.config import API_URL
from website.utils.db import db
from website.view.view import (page_not_found_with_error_in_page, page_not_found_with_error, 
                        first_page_warning, last_page_warning, go_to_next_page, go_to_prev_page, page_not_found_with_error_in_page, 
                        database_save_error_alert, homepage_search_redirect, logout_redirect, render_homepage_template) 
from website.controllers.search_controller import search_results
from website.models.wishlist_user_model import Wishlist_user
from website.models.movie_model import Movies
import requests

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

def get_url(search_result):
    if search_result:
        url = API_URL + "&query=" + search_result 

    else:
        url = API_URL + "&query=default"

    return url

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

    search_response = handle_search(results)
    if search_response:
        return search_response
    
    if results['current_service'] == "results":
        return navigate_page(results['search_result'], results['current_page'], results['total_pages'], 'results.results_search_list')
    
    elif results['current_service'] == "wishlist":
        return navigate_page(results['search_result'], results['current_page'], results['total_pages'], 'wishlist.wishlist_pages')

    # Handles pagination
    return homepage_search_redirect()

def navigate_page(search_result, current_page, total_pages, current_service):

    """
    Handles navigation through pages for the movie search results.

    Returns:
        Response: Redirect to the next or previous page.
    """

    if request.form.get('npage') == 'Next':

        if current_page >= total_pages:
            last_page_warning()

        current_page += 1
        return go_to_next_page(search_result, current_page, current_service)

    elif request.form.get('ppage') == 'Prev':

        if current_page <= 1:
            first_page_warning(search_result)

        current_page -= 1
        return go_to_prev_page(search_result, current_page, current_service)

def handle_search(results):
    """
    Handles the search form submission if any.

    Returns:
        Response: Redirect to search results or homepage.
    """
    search_text = request.form.get('search')

    if 'search' in request.form:
        if search_text != "":
                
            if results['current_service'] == "results":
                return navigate_page(results['search_result'], results['current_page'], results['total_pages'], 'results.results_search_list')

            elif results['current_service'] == "wishlist":
                return navigate_page(results['search_result'], results['current_page'], results['total_pages'], 'wishlist.wishlist_search_list')

            else:
                return navigate_page(results['search_result'], results['current_page'], results['total_pages'], 'homepage.search')
    else:
        return homepage_search_redirect()
    
def handle_logout():
    """
    Handles the logout form submission.
    """

    if request.form.get('logout') == 'Log Out':
            # session_logout_warning(session['username'])
            return logout_redirect()

def get_set_of_movies(movie_list, current_page, search_result, current_service):
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
            "search_result": search_result,
            "current_service": current_service
        }
    except ValueError as e:
        page_not_found_with_error(e)
        return {
            "movie_set": [],
            "total_pages": movies.total_pages,
            "current_page": current_page,
            "search_result": search_result
        }


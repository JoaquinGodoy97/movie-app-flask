from flask import request, jsonify
from website.utils.settings import API_URL
from website.view.view import (page_not_found_with_error_in_page, page_not_found_with_error, 
                        first_page_warning, last_page_warning, wishlist_pages_redirect, wishlist_search_redirect,
                        page_not_found_with_error_in_page, homepage_search_redirect, logout_redirect, results_pages_redirect, first_page_warning_wishlist) 
from website.models.movie_model import Movies
import requests
from website.utils.logger import logger

def get_url(search_result):
    if search_result:
        url = API_URL + "&query=" + search_result 

    else:
        url = API_URL + "&query=default"

    return url

def fetch_movie_results(search_result):
    """
    Fetches movie results from the API.

    Returns:
        dict: JSON response containing movie results.
    """
    try:
        api_url_for_search_results = get_url(search_result)
        response = requests.get(api_url_for_search_results)

    except Exception as e:
        # Log the exception details for internal use
        logger.error(f"An error occurred: {e}")  # Log the exception
        # Return a generic error message to the client
        return jsonify({"error": "An internal error occurred. Please try again later."}), 500
    
    
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
                        'mv_id': movie.get('id'),
                        'title': movie.get('title'),
                        'poster_path': movie.get('poster_path'),
                        'overview': movie.get('overview')
                    }

                    all_movie_results.append(movie_data)
                    
        except requests.exceptions.RequestException as e:
            page_not_found_with_error_in_page(page, e)
            continue

    return all_movie_results

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
        return navigate_page(results['search_result'], results['current_page'], results['total_pages'], 'results')
    
    elif results['current_service'] == "wishlist":
        return navigate_page(results['search_result'], results['current_page'], results['total_pages'], 'wishlist')

    # Handles pagination
    # return homepage_search_redirect()

def navigate_page(search_result, current_page, total_pages, current_service):

    """
    Handles navigation through pages for the movie search results.

    Returns:
        Response: Redirect to the next or previous page.
    """

    if request.form.get('npage') == 'Next':
        if current_page < total_pages:
            current_page += 1
            
            if current_page == total_pages:
                last_page_warning()

    elif request.form.get('ppage') == 'Prev':
        if current_page > 1:
            current_page -= 1

            if current_service == 'results':
                if current_page == 1:
                    first_page_warning(search_result)
            
            elif current_service == "wishlist" and current_page == 1:
                first_page_warning_wishlist()

    # Handle Wishlist pagination with and without search results
    if current_service == "wishlist":
        if search_result:
            return wishlist_search_redirect(current_page, search_result)
        else:
            return wishlist_pages_redirect(current_page)
    # Handle Results pagination
    elif current_service == "results":
        return results_pages_redirect(current_page, search_result)

    return None
def handle_search(results):
    """
    Handles the search form submission if any.

    Returns:
        Response: Redirect to search results or homepage.
    """
    search_text = request.form.get('search')

    if 'search' in request.form:
        if search_text != "":

            if results['search_result'] != search_text:
                    results['search_result'] = search_text 
                    results['current_page'] = 1
                
            if results['current_service'] == "results":
                return navigate_page(results['search_result'], results['current_page'], results['total_pages'], 'results')

            elif results['current_service'] == "wishlist":
                
                return navigate_page(results['search_result'], results['current_page'], results['total_pages'], 'wishlist')

            else:
                return navigate_page(results['search_result'], results['current_page'], results['total_pages'], 'homepage.search')
    else:
        # return homepage_search_redirect()
        None
    
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
            "movie_set": movies.get_movies_by_page(current_page, current_service),
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


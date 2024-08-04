from flask import session, Blueprint, request
from website.config import API_URL
from website.models.wishlist_user_model import Wishlist_user
from website.controllers.wishlist_controller import add_to_wishlist_db
import requests

results = Blueprint('results', __name__)

@results.route('/results/<search_result>/<int:current_page>' , methods=["GET", "POST"])
def results_search_list(search_result, current_page):

    from website.view import logout_redirect, display_movies, homepage_search_redirect, page_not_found

    # print("this is the page number in results" + current_page)

    api_url_for_search_results = get_url(search_result)

    # Request.response Obj
    response = requests.get(api_url_for_search_results)

    """
    # Into a Dict Alternative
    # movies = json.loads(response.text) 
    global movies
    """
    
    movie_results_no_page_separation = response.json() # same result

    if not movie_results_no_page_separation['results']:
        page_not_found()
        return homepage_search_redirect()
        
    movies = fetch_multiple_pages(search_result, start_page=1, total_pages=movie_results_no_page_separation['total_pages'])
    movie_results = get_set_of_movies(movies, current_page, search_result)

    if request.method == 'POST':
        
        response = handle_form(movie_results)

        if response:
            return response

    else:
        if "username" not in session:
            logout_redirect()

    return display_movies(movie_results, template_success='results.html', template_error='index.html')
    
    # return render_template('results.html', url_view=api_url_for_search_results, movies=movies_per_page, search_result=search_result, current_page=current_page, movie_pages_numb= movie_pages_numb)



@results.route('/results/<search_result>/<int:current_page>/<movie_name>/<int:movie_id>' , methods=["GET", "POST"])
def add_to_wishlist(search_result, current_page, movie_name, movie_id):

    from website.view import alert_movie_already_added, display_current_results, database_wishlist_save_success_alert

    movie_exists = Wishlist_user.query.filter_by(user_id=session['username'], mv_id=movie_id).first()

    if movie_exists:
        alert_movie_already_added(movie_name, movie_id)

    else:
        database_wishlist_save_success_alert(movie_name, movie_id)
        add_to_wishlist_db(movie_id, movie_name, user_id=session['username'])

    # if movie is not repeated then add
    return display_current_results(search_result, current_page)

def movies_dict(movies_per_pages): #Movies Per Pages
    movies_list = []

    for movie_set in movies_per_pages:
        for page_number in range(1, len(movies_per_pages) + 1):
            
            movies_page = {
                'movie_set': movie_set,
                'page_number': page_number,
            }
            movies_list.append(movies_page)
            break
        
    return movies_list

def get_url(search_result):
    if search_result:
        url = API_URL + "&query=" + search_result 

    else:
        url = API_URL + "&query=default"
        # search = ''
    
    return url

"""
# Handles navigation Through pages button "NEXT" and "PREVIOUS" with edge cases
"""

def navigate_page(search_result, current_page, total_pages):

    from website.view import first_page_warning, last_page_warning, go_to_next_page, go_to_prev_page

    if request.form.get('npage') == 'Next':

        if current_page == total_pages - 1:
            last_page_warning()

        current_page = current_page + 1
        return go_to_next_page(search_result, current_page)

    elif request.form.get('ppage') == 'Prev':

        if current_page == 2:
            first_page_warning(search_result)

        current_page = current_page - 1
        return go_to_prev_page(search_result, current_page)

"""
# Handles search if any. Else redirects to homepage.
"""
        
def handle_search():
    
    from .search_controller import search
    from website.view import homepage_search_redirect

    search_text = request.form.get('search')

    if 'search' in request.form:
        if search_text != "":
            return search()
    else:
        return homepage_search_redirect()

"""
# Handles logout session. Includes warning message.
"""
            
def handle_logout():

    from website.view import logout_redirect

    if request.form.get('logout') == 'Log Out':
            # session_logout_warning(session['username'])
            return logout_redirect()

"""
# Handle form submissions for logout, search, and pagination.

# Returns:
#     A response for logout or search if applicable, otherwise None.
"""
    
def handle_form(results):
    
    # Handle logout
    logout_response = handle_logout()
    if logout_response:
        return logout_response

    # Handle search
    search_response = handle_search()
    if search_response:
        return search_response

    # Handle pagination
    return navigate_page(results['search_result'], results['current_page'], results['total_pages'])
    # return None # ?????????????????????????????????????????????

"""
    # Get a set of movies in an organized manner for later display.
"""

def get_set_of_movies(movie_list, current_page, search_result):

    from website.models.movie_model import Movies
    from website.view import page_not_found_with_error

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

    from website.view import page_not_found_with_error_in_page
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
from flask import Blueprint, render_template, request, url_for, redirect, session, jsonify, json
from .results_controller import handle_form, get_set_of_movies
from server.models.wishlist_user_model import Wishlist_user
from server.view.view import (invalid_token, display_movies, wrong_movie_request, 
                    movies_limit_reached_database, movie_already_added, movie_removed_success,
                    movie_added_success, get_movies_status)
from server.services.auth_services import Security
from server.services.wishlist_services import (get_results_by_movie_id, add_to_wishlist_db, remove_from_wishlist_db,
                                                filter_by_usersession_and_movieid, filter_by_usersession, is_wishlist_user_limit_reached,
                                                bring_single_movie_by_user, filter_movies_by_search_if_any, bring_multiple_movies_by_user, wishlist_filter_query_by_movie_id)
wishlist = Blueprint('wishlist', __name__)

@wishlist.route('/wishlist', methods=["GET"])
# @login_required
def wishlist_pages():

    has_acess = Security.verify_token(request.headers)
    
    if not has_acess:
        return invalid_token()
    
    search_result = request.args.get('query', '')
    current_page = request.args.get('page', 1, type=int)

    results = filter_by_usersession(has_acess['username'])

    # if not results:
    #     alert_no_movie_added_wishlist()
    #     return render_wishlist_template()
    # return jsonify({ "message": results })
    
    results = get_results_by_movie_id(results)
    # print("2st results filter:",results)

    current_service = 'wishlist'
    search_result = ""
    movie_results = get_set_of_movies(results, current_page, search_result, current_service)

    return display_movies(movie_results, render_success='/wishlist', render_error='/wishlist')

@wishlist.route('/wishlist/add/<int:movie_id>/<movie_name>', methods=["POST"])
# @login_required
def add_to_wishlist(movie_id, movie_name):

    """
    Adds a movie to the user's wishlist if it doesn't already exist.

    Returns:
        Response: Rendered template with the updated results.
    """

    has_acess = Security.verify_token(request.headers)
    
    if not has_acess:
        return invalid_token()
    
    if not movie_id or not movie_name:
        return wrong_movie_request()

    user = has_acess['username']
    # return jsonify({ "message": f"{session['username']} added {movie_name} to wishlist"})

    movie_exists = filter_by_usersession_and_movieid(user, movie_id)

    print(movie_exists, "CHeck if movie exists")
    if movie_exists:
        remove_from_wishlist_db(movie_exists)
        # alert_movie_already_added(movie_name, movie_id)
        return movie_already_added()
    else:

        if is_wishlist_user_limit_reached(user):
            return movies_limit_reached_database()
        
        add_to_wishlist_db(movie_id, movie_name, username=user)
    
    return movie_added_success(user, movie_name)

@wishlist.route('/wishlist/remove/<int:movie_id>', methods=["POST"])
# @login_required
def remove_from_wishlist(movie_id):
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
    has_acess = Security.verify_token(request.headers)

    if not has_acess:
        return invalid_token()
    
    # found_movie_to_delete = Wishlist_user.query.filter_by(mv_id=movie_id).first()
    found_movie_to_delete = wishlist_filter_query_by_movie_id(movie_id)

    print(found_movie_to_delete, "found movie to delete? no? yes?")
    if found_movie_to_delete:
        remove_from_wishlist_db(movie_id)
        return movie_removed_success()
    else:
        return wrong_movie_request()
    # return redirect(url_for("wishlist.wishlist_pages", current_page=current_page))

@wishlist.route('/wishlist/search', methods=["GET"])
# @login_required
def wishlist_search():

    has_acess = Security.verify_token(request.headers)
    
    if not has_acess:
        return invalid_token()

    search_result = request.args.get('query', '')
    current_page = request.args.get('page', 1, type=int)
    
    results = filter_by_usersession(has_acess['username'])
    # return jsonify({ "message": results})
    results = get_results_by_movie_id(results)
    results = filter_movies_by_search_if_any(results, search_result)
    # # return jsonify({ "message": results})

    movie_results = get_set_of_movies(results, current_page, search_result, current_service='wishlist')

    if movie_results['movie_set'] == None:
        movie_results['movie_set'] = ''
    
    return display_movies(movie_results, render_success="/wishlist/search", render_error="/wishlist")
    # return redirect(url_for("wishlist.wishlist_search", current_page=current_page, search_result=search_result))

"""
(FRONT)CHECKS FOR BUTTON PRESSED
(BACK) IF IT WAS SAVED INTO WISHLIST THEN SEND THE MOVIE IF IT'S IN DB OF USER.
"""

@wishlist.route('/wishlist-status', methods=['POST'])
# @login_required
def wishlist_status():
    token = Security.verify_token(request.headers)

    if not token:
        return invalid_token()
    
    user = token['username']

    movie_ids = request.json.get('movie_ids')  # Accept a list of movie IDs
    # Fetch all wishlist statuses for the user in one query
    statuses = bring_multiple_movies_by_user(user, movie_ids)
    
    # is_in_wishlist = bring_single_movie_by_user(user, movie_id)
    # return jsonify({'in_wishlist': is_in_wishlist})
    return get_movies_status(statuses)
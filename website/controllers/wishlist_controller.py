from flask import Blueprint, render_template, request, url_for, redirect, session, flash
from website.models.wishlist_user_model import Wishlist_user
from website.utils.db import db
from website.config import BASE_URL, API_KEY
import requests

wishlist = Blueprint('wishlist', __name__)

@wishlist.route('/wishlist', methods=["POST", "GET"])
def wishlist_homepage(current_page = 1):
    return redirect(url_for('wishlist.wishlist_pages', current_page=current_page))


@wishlist.route('/wishlist/<int:current_page>', methods=["POST", "GET"])
def wishlist_pages(current_page):

    from .results_controller import handle_form, get_set_of_movies
    from website.view import session_logout_warning, logout_redirect, display_movies, wishlist_redirect, alert_no_movie_added_wishlist

    if "username" not in session:
        return logout_redirect()

    results = Wishlist_user.query.filter_by(user_id=session['username']).all()

    if not results:
        alert_no_movie_added_wishlist()
        return render_template('wishlist.html')

    for movie in results:
        api_url = BASE_URL + "/movie/" + str(movie.mv_id) + "?" + API_KEY
        
        response = requests.get(api_url)
        response.raise_for_status()  # Check for HTTP request errors
        results_json = response.json()
        
        # Update movie_data fields
        movie.title = results_json.get('title')
        movie.poster_path = results_json.get('poster_path')
        movie.overview = results_json.get('overview')
    
    movie_results = get_set_of_movies(results, current_page, search_result="")

    if current_page > movie_results['total_pages']:
        return wishlist_redirect()

    if request.method == 'POST':

        print('post')

        response = handle_form(movie_results)

        if response:
            return response

        #LOG OUT
        if request.form.get('logout') == 'Log Out':
            session_logout_warning(session['username'])
            return logout_redirect()
        
    return display_movies(movie_results, template_success='wishlist.html', template_error='wishlist.html')

@wishlist.route('/wishlist/<int:current_page>/<int:movie_id>/<movie_name>', methods=["POST", "GET"])
def remove_from_wishlist(current_page, movie_id, movie_name):

    from website.view import database_delete_error_alert, database_wishlist_delete_erorr_alert
    
    found_movie_to_delete = Wishlist_user.query.filter_by(mv_id=str(movie_id)).first()

    if found_movie_to_delete:
        try:
            db.session.delete(found_movie_to_delete)
            db.session.commit()
            print(found_movie_to_delete)
            database_wishlist_delete_erorr_alert(movie_name, movie_id)

        except Exception as e:
            db.session.rollback()
            database_delete_error_alert(e)
        finally:
            db.session.close()

    return redirect(url_for("wishlist.wishlist_pages", current_page=current_page))

def add_to_wishlist_db(movie_id, movie_name, user_id):

    from website.view import database_save_error_alert

    try:
        user_data = Wishlist_user(mv_id=movie_id, title=movie_name, user_id=user_id)
        db.session.add(user_data)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        database_save_error_alert(e)

    finally:
        db.session.close()
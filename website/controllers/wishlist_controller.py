from flask import Blueprint, render_template, request, url_for, redirect, session
from .results_controller import handle_form, get_set_of_movies
from website.models.wishlist_user_model import Wishlist_user
from website.utils.db import db
from website.config import BASE_URL, API_KEY
from website.view.view import (database_save_error_alert, session_logout_warning, logout_redirect, display_movies, wishlist_redirect, 
                    alert_no_movie_added_wishlist, database_delete_error_alert, database_wishlist_delete_erorr_alert)
from website.services.auth_services import is_user_logged_in
from website.services.wishlist_services import get_results_by_movie_id

wishlist = Blueprint('wishlist', __name__)

@wishlist.route('/wishlist', methods=["POST", "GET"])
def wishlist_homepage(current_page = 1):
    return redirect(url_for('wishlist.wishlist_pages', current_page=current_page))

@wishlist.route('/wishlist/<int:current_page>', methods=["POST", "GET"])
def wishlist_pages(current_page):

    if is_user_logged_in(session) == False:
        return logout_redirect()

    results = Wishlist_user.query.filter_by(user_id=session['username']).all()

    if not results:
        alert_no_movie_added_wishlist()
        return render_template('wishlist.html')
    
    results = get_results_by_movie_id(results)
    search_result = ''
    movie_results = get_set_of_movies(results, current_page, search_result, current_service='wishlist')

    if current_page > movie_results['total_pages']:
        return wishlist_redirect()

    if request.method == 'POST':

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
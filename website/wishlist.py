from flask import Blueprint, render_template, request, url_for, redirect, session, flash
import requests, json
from .results import paginate
from .models.wishlist_user_data import Wishlist_user_data
from .models.user import User
from website.utils.db import db

wishlist = Blueprint('wishlist', __name__)

@wishlist.route('/wishlist', methods=["POST", "GET"])
def wishlist_homepage(page_num = 1):
    return redirect(url_for('wishlist.wishlist_pages', page_num=page_num))


@wishlist.route('/wishlist/<int:page_num>', methods=["POST", "GET"])
def wishlist_pages(page_num):

    # if no movies in movie list "sorry no items added to wishlist"
    from .results import BASE_URL, API_KEY
    from .results import paginate, movies_dict

    results = Wishlist_user_data.query.filter_by(user_id=session['username']).all()

    for movie in results:
        # https://api.themoviedb.org/3/movie/343611?api_key=API_KEY
        # https://api.themoviedb.org/3/movie/23446?api_key=52495a0d2fceefe863149757f96d5d21
        api_url = BASE_URL + "/movie/" + str(movie.mv_id) + "?" + API_KEY
        
        response = requests.get(api_url)
        response.raise_for_status()  # Check for HTTP request errors
        results_json = response.json()
        
        # Update movie_data fields
        movie.title = results_json.get('title')
        movie.poster_path = results_json.get('poster_path')
        movie.overview = results_json.get('overview')

    if request.method == 'POST':

        #NEXT AND PREVIOUS PAGE // PAGINATION

        if request.form.get('npage') == 'Next':

            set_of_movies = len(paginate(results))

            if page_num >= set_of_movies:
                pass
            
            else:
                if page_num == set_of_movies - 1:
                    flash('You have reached the last page. Please go back if you want to look for more results.', 'warning')
                    pass

                page_num = page_num + 1
                return redirect(url_for('wishlist.wishlist_pages', page_num=page_num))

        elif request.form.get('ppage') == 'Prev':

            if page_num == 1:
                pass
            else:
                if page_num == 2:
                    flash('Right now you are on the first page of your wishlist.', 'warning') 

                page_num = page_num - 1
                return redirect(url_for('wishlist.wishlist_pages', page_num=page_num))

        #LOG OUT

        if request.form.get('logout') == 'Log Out':
            flash(f"{session['username']} has been logged out", "dark")

            return redirect(url_for('auth.logout'))
        
    else:

        #CHECK FOR USER IN SESSION

        if "username" not in session:
            return redirect(url_for('auth.logout'))
        
    #CHUNKS OF MOVIES // MAKE CHUNKS OF 5
        
    if len(results) > 0:
            movies_per_page = movies_dict(paginate(results))
            movie_pages_numb = len(movies_per_page) # page length
            movies_per_page = movies_per_page[page_num - 1]['movie_set'] # movie_set by page

    else:
        movies_per_page = []
        flash("Page not found.", "warning")
        movie_pages_numb = 0
        return render_template('index.html')
    
    # return clean_results
    return render_template('wishlist.html', movies=movies_per_page, page_num=page_num, movie_pages_numb=movie_pages_numb)

#TRANSFORMAR FLASK EN UNA API REST y PROBAR USAR REACT COMO FRONT END 

@wishlist.route('/wishlist/<int:page_num>/<movie_id>', methods=["POST", "GET"])
def remove_from_wishlist(page_num, movie_id):


    found_movie_to_delete = Wishlist_user_data.query.filter_by(mv_id=str(movie_id)).first()

    print(movie_id, ": if any movie")

    if found_movie_to_delete:
        try:
            db.session.delete(found_movie_to_delete)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred while saving to the database: {str(e)}", "danger")
        finally:
            db.session.close()

    return redirect(url_for("wishlist.wishlist_pages", page_num=page_num))
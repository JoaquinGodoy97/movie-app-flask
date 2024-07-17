from flask import Blueprint, render_template, request, url_for, redirect, session, flash
import requests, json
from .models.wishlist_user_data import Wishlist_user_data
from website.utils.db import db

# Blueprint #has a lot of roots inside it 

results = Blueprint('results', __name__)

API_KEY = 'api_key=52495a0d2fceefe863149757f96d5d21'
BASE_URL = 'https://api.themoviedb.org/3'
API_URL = BASE_URL + '/search/movie?' + API_KEY

counter = 0
postcounter = counter + 5

def paginate(movies): #Paginating results
    movie_set_list = []

    #Make a Set of 5 in 5
    for movie_set in range(0, len(movies), 5):
        movie_set_end = movie_set + 5
        movie_set_list.append(movies[movie_set:movie_set_end])
    
    return movie_set_list

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

@results.route('/results/<search_result>/<int:page_num>' , methods=["GET", "POST"])
def results_search_list(search_result, page_num):

    # print("this is the page number in results" + page_num)
    from .homepage import search

    search_text = request.form.get('search')

    if search_result:

        r_json = API_URL + "&query=" + search_result  

    else:
        r_json = API_URL + "&query=default"
        search = ''
    
    response = requests.get(r_json) # request.response Obj
    # movies = json.loads(response.text) # into a dicts
    global movies
    results = response.json() # same result
    movies = results['results']

    if request.method == 'POST':

        #next and prev button 
        
        if request.form.get('npage') == 'Next':

            set_of_movies = len(paginate(movies))

            if page_num >= set_of_movies:
                pass
            
            else:
                if page_num == set_of_movies - 1:
                    flash('You have reached the last page. Please go back if you want to look for more results.', 'warning')
                    pass

                page_num = page_num + 1
                return redirect(url_for('results.results_search_list', search_result=search_result, page_num=page_num))

        elif request.form.get('ppage') == 'Prev':

            if page_num == 1:
                pass
            else:
                if page_num == 2:
                    flash('Right now you are on the first page of ' + "\"" + search_result + "\" results.", 'warning') 

                page_num = page_num - 1
                return redirect(url_for('results.results_search_list', search_result=search_result, page_num=page_num))
            
        elif request.form.get('logout') == 'Log Out':
            flash(f"{session['username']} has been logged out", "dark")
            return redirect(url_for('auth.logout'))    
        
        elif 'search' in request.form:
                if search_text != "":
                    return search()
                else:
                    return redirect(url_for("homepage.search"))
                
        
        
        else:
            pass
    else:
        if "username" not in session:
            return redirect(url_for('auth.logout'))
    
    if len(movies) > 0:
        movies_per_page = movies_dict(paginate(movies))
        movie_pages_numb = len(movies_per_page) # page length
        movies_per_page = movies_per_page[page_num - 1]['movie_set'] # movie_set by page

    else:
        movies_per_page = []
        flash("Page not found.", "warning")
        movie_pages_numb = 0
        return render_template('index.html')

    # print(len(movies['results'])) #send the length of the results  
    
    return render_template('results.html', url_view=r_json, movies=movies_per_page, search_result=search_result, page_num=page_num, movie_pages_numb= movie_pages_numb)

# ADDING ITEMS TO WISHLIST -------------------------------------------------

@results.route('/results/<search_result>/<int:page_num>/<movie_name>/<int:movie_id>' , methods=["GET", "POST"])
def add_to_wishlist(search_result, page_num, movie_name, movie_id):

    movie_exists = Wishlist_user_data.query.filter_by(user_id=session['username'], mv_id=movie_id).first()

    if movie_exists:
        flash(f"Cannot add {movie_name, movie_id } to the Wishlist. Already added.", 'danger')
    else:

        try:

            user_data = Wishlist_user_data(mv_id=movie_id, title=movie_name, user_id=session['username'])
            db.session.add(user_data)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred while saving to the database: {str(e)}", "danger")

        finally:
            db.session.close()

    # if movie is not repeated then add
    
    flash(f"Added {movie_name, movie_id } to the Wishlist. Also this is the length of object movies.", 'success')
    return redirect(url_for("results.results_search_list", search_result=search_result, page_num=page_num))

#ADD IF RESULT IS /40000 page and doesnt exist


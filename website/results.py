from logging import warning
from flask import Blueprint, render_template, request, url_for, redirect, session, flash
import requests, json

# Blueprint #has a lot of roots inside it 

results = Blueprint('results', __name__)

API_KEY = 'api_key=52495a0d2fceefe863149757f96d5d21'
BASE_URL = 'https://api.themoviedb.org/3'
API_URL = BASE_URL + '/search/movie?' + API_KEY

counter = 0
postcounter = counter + 5

def paginate(movies):
    movie_set_list = []
    movies_results = movies['results']

    #make a set of 5 in t5
    for movie_set in range(0, len(movies_results), 5):
        movie_set_end = movie_set + 5
        movie_set_list.append(movies['results'][movie_set:movie_set_end])
    
    return movie_set_list

def movies_dict(m_p_pages):
    movies_dict_list = []
    for m_p in m_p_pages:
        for page_number in range(1, len(m_p_pages) + 1):
            
            movies_page = {
                'movie_set': m_p,
                'page_number': page_number,
            }
            movies_dict_list.append(movies_page)

            break
        
    return movies_dict_list

@results.route('/results/<search_result>/<int:page_num>' , methods=["GET", "POST"])
def search_list(search_result, page_num):

    # print("this is the page number in results" + page_num)
    from .home import search

    search_text = request.form.get('search')

    if search_result:

        r_json = API_URL + "&query=" + search_result  

    else:
        r_json = API_URL + "&query=default"
        search = ''
    
    response = requests.get(r_json) # request.response Obj
    movies = json.loads(response.text) # into a dict

    if request.method == 'POST':

        #next and prev button 
        
        #fixed problem of alerts
        
        if request.form.get('npage') == 'Next':

            if page_num >= len(paginate(movies)):
                pass
            
            else:
                if page_num == len(paginate(movies)) - 1:
                    flash('You have reached the last page. Please go back if you want to look for more results.')
                    pass

                page_num = page_num + 1
                return redirect(url_for('results.search_list', search_result=search_result, page_num=page_num))

        elif request.form.get('ppage') == 'Prev':

            if page_num == 1:
                pass
            else:
                if page_num == 2:
                    flash('Right now you are on the first page of ' + "\"" + search_result + "\" results.") 

                page_num = page_num - 1
                return redirect(url_for('results.search_list', search_result=search_result, page_num=page_num))
        else:
            if 'search' in request.form:
        
                if search_text != "":
                    return search()
                    
                else:
                    return render_template('index.html')
    else:
        pass
    
    if len(movies['results']) > 0:
        movies_per_page = movies_dict(paginate(movies))
        movie_pages_numb = len(movies_per_page) # page length
        movies_per_page = movies_per_page[page_num - 1]['movie_set'] # movie_set by page

    else:
        movies_per_page = []
        flash("Page not found.")
        movie_pages_numb = 0
        return render_template('index.html')

    # print(len(movies['results'])) #send the length of the results  
    
    return render_template('results.html', url_view=r_json, movies=movies_per_page, search_result=search_result, page_num=page_num, movie_pages_numb= movie_pages_numb)



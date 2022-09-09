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
    
    # if r_json:

    #     # response = requests.get(r_json) # request.response Obj
    #     # movies = json.loads(response.text) # into a dict

    #     # if npage:
    #     #     print('pressed!')
    #     #     # print(counter)
    #     #     # counter += 2
    #     #     # postcounter = counter + 4
    #     #     # movies_results = movies['results'][counter:postcounter]
            
    #     #     # return redirect(url_for('results.search_list.page2', search_result))

    #     # else:
    #     movies_results = movies['results'][0:5]
    # else:
    #     pass

    npage = request.form.get('npage')
    ppage = request.form.get('ppage')
    
    if request.method == 'POST':

        if request.form.get('npage') == 'Next':
            print("NEXT pressed")

            if page_num >= len(paginate(movies)):
                flash('You have reached the last page. Please go back if you want to look for more results.')
                pass
            else:
                print('increase 1')
                page_num = page_num + 1
                return redirect(url_for('results.search_list', search_result=search_result, page_num=page_num))

        elif request.form.get('ppage') == 'Prev':
            print("PREV pressed")

            if page_num <= 1:
                flash('Right now you are on the first page of ' + "\"" + search_result + "\" results.") 
                pass
            else:
                # print('button was pressed asdasd')
                page_num = page_num - 1
                return redirect(url_for('results.search_list', search_result=search_result, page_num=page_num))
        else:
            pass

        if 'search' in request.form:
        
            if search_text != "":
                return search()
                
            else:
                return render_template('index.html' )
    else:
        pass

    print('ignore the button')

    movies_per_page_dict = movies_dict(paginate(movies))

    movies_per_page_dict = movies_per_page_dict[page_num - 1]['movie_set']
    
    return render_template('results.html', url_view=r_json, movies=movies_per_page_dict, search_result=search_result, page_num=page_num)

@results.route('/results/<search_result>/<page>', methods=["GET", "POST"])
def nextpage(search_result, page):

    return render_template('results.html' )


# def paginate(movies, counter):

#     print(len(movies['results'][counter:])) # 20 for "live" search if len is not the same

#     def countup(counter):
#         counter =+ 5
#         postcounter = counter + 5
#         return counter

#     def countdown(counter):
#         counter =- 5
#         return counter

#     # postcounter = counter + 5
#     if 'npage' in request.form:
#         print('nextpage inside counterfunction')
#         print(counter)
#         counter = countup(counter)
#         return movies['results'][counter:postcounter]
    
#         # print(movies['results'][counter:postcounter])

#     else:
#         print('previus inside counterfunction')
#         print(counter)
#         counter = countdown(counter)
#         return movies['results'][counter:postcounter]



from flask import Blueprint, render_template, request, url_for, redirect, session
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



@results.route('/results/<search_result>', methods=["GET", "POST"])
def search_list(search_result):


    from .home import search

    search_text = request.form.get('search')
    # # npage = request.form['npage']


    if search_result:
        r_json = API_URL + "&query=" + search_result  

        # return app.add_url_rule(searchPlus, 'index', index)
    else:
        r_json = API_URL + "&query=default"
        search = ''
    
    response = requests.get(r_json) # request.response Obj
    movies = json.loads(response.text) # into a dict


    if r_json:

        # response = requests.get(r_json) # request.response Obj
        # movies = json.loads(response.text) # into a dict

        # if npage:
        #     print('pressed!')
        #     # print(counter)
        #     # counter += 2
        #     # postcounter = counter + 4
        #     # movies_results = movies['results'][counter:postcounter]
            
        #     # return redirect(url_for('results.search_list.page2', search_result))

        # else:
        movies_results = movies['results'][0:5]
    else:
        pass
    

    if 'search' in request.form:
    
        if search_text != "":
            return search()
            
        else:
            if 'npage' or 'ppage' in request.form:
                print('Go to the next page!')
                
                # movies_results = paginate(movies, counter)

                # return redirect(url_for("results.nextpage", page_number=1, search_result=search_result))
                return render_template("results.html", movies=movies_results)

            else:
                pass

            print('Text empty')
            return redirect(url_for('home.search'))
    else:
        pass
    

    # if npage:
    #     print('you pressed it out of the scope')  

    # response = requests.get(r_json) # request.response Obj
    # movies = json.loads(response.text) # into a dict

    
    print('ignore the button')

    movie_set_list = paginate(movies) # movies separated per set
    

    return render_template('results.html', url_view=r_json, movies=movie_set_list[1], search_result=search_result)

@results.route('/results/<search_result>/<page_number>', methods=["GET", "POST"])
def nextpage(search_result, number_page):

    from .home import render_results

    #this is repeated could be summarised
    
    new_search_result = API_URL + "&query=" + search_result
    api_data = render_results(new_search_result)

    response = requests.get(new_search_result) # request.response Obj
    movies = json.loads(response.text)
    
    movie_set_list = paginate(movies)
    
    movies_final = movie_set_list # [int(page_number) - 1]
    session['pagetotal'] = movies_final
    # print(movies_final)

    return render_template('results.html', url_view=api_data, movies=movies_final )


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



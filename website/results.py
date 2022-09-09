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

        # return app.add_url_rule(searchPlus, 'index', index)
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
                pass
            else:
                print('increase 1')
                page_num = page_num + 1
                return redirect(url_for('results.search_list', search_result=search_result, page_num=page_num))

        elif request.form.get('ppage') == 'Prev':
            print("PREV pressed")

            if page_num <= 1:
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
                pass
                # if 'npage' or 'ppage' in request.form:
                    # print('Go to the next page!')
                    
                    # movies_results = paginate(movies, counter)

                    # return redirect(url_for("results.nextpage", page_number=1, search_result=search_result))
                    # return render_template("results.html", movies=movies_results)
    else:
        pass

    print('ignore the button')

    movies_per_page_dict = movies_dict(paginate(movies))

    # print(movies_per_page_dict[page_num ])

    movies_per_page_dict = movies_per_page_dict[page_num - 1]['movie_set']
    

    # movies = Movie_pages(page, paginate(movies)) # movies separated per set
    

    return render_template('results.html', url_view=r_json, movies=movies_per_page_dict, search_result=search_result, page_num=page_num)

@results.route('/results/<search_result>/<page>', methods=["GET", "POST"])
def nextpage(search_result, page):

    print("the page number in nextpage is " + page)

    from .home import render_results

    #this is repeated could be summarised
    
    new_search_result = API_URL + "&query=" + search_result
    api_data = render_results(new_search_result)

    response = requests.get(new_search_result) # request.response Obj
    movies = json.loads(response.text)
    
    movie_set_list = paginate(movies)
    
    movies_final = movie_set_list # [int(page_number) - 1]
    # session['pagetotal'] = movies_final
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



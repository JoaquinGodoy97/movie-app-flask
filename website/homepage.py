from flask import Flask, render_template, request, redirect, url_for, Blueprint, session, flash

homepage = Blueprint('homepage', __name__)

# API_KEY = 'api_key=52495a0d2fceefe863149757f96d5d21'
# BASE_URL = 'https://api.themoviedb.org/3'
# API_URL = BASE_URL + '/search/movie?' + API_KEY


# DATA BASE
# app = Flask(__name__) 
# app.config['SECRET_KEY'] = "secretkeycreated"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# r_json = API_URL + "&query=default"
# x = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"



def render_results(search):
    list_without_space = search.split() #result into a list 

    search_split_by_plus = "+".join(list_without_space)
    return search_split_by_plus

@homepage.route('/search', methods=['GET', 'POST']) # change the route by "/" to make it default /search
def search():
    x = "***************************************************"
    search_plus = ""
    
    search = request.form.get('search') ## apparently request.form .from() creates an html form for capturing the data
    
    if request.method == 'POST':

        
        
        
        if 'npage' in request.form:
            print('pressed from homepage!')

        elif request.form.get('logout') == 'Log Out':
                flash(f"{session['username']} has been logged out", "dark")
                return redirect(url_for('auth.logout'))
            
        elif search:
            
            if search == "":
                print(x)
                return redirect(url_for("homepage.search")) # default search
            
            else:
                search_plus = render_results(search)
                return redirect(url_for('results.results_search_list', search_result=search_plus, page_num=1))
            
    else:
        if "username" not in session:
            return redirect(url_for('auth.logout'))

    
    return render_template('index.html')



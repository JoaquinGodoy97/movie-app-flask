from urllib import response
from flask import Flask, flash, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import json, requests


API_KEY = 'api_key=52495a0d2fceefe863149757f96d5d21'
BASE_URL = 'https://api.themoviedb.org/3'
API_URL = BASE_URL + '/search/movie?' + API_KEY

x = "***************************************************"

# DATA BASE
app = Flask(__name__)
# app.config['SECRET_KEY'] = "secretkeycreated"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

r_json = API_URL + "&query=default"

@app.route('/', methods=['GET', 'POST'])
def index():

    search = request.form.get('search')
    npage = request.form.get('npage')
    # counter = 0
    

    r_json = API_URL + "&query=default"

    if search:
        app.add_url_rule('/search', "search", search)


    return render_template('index.html', urlView=r_json,  search=search)


    

def search():

    searchPlus = ""
    

    if search:

        listNoSpace = search.split()

        for i in range(0,len(listNoSpace)):
            searchPlus += str(listNoSpace[i])
        
            if i < len(listNoSpace) - 1:
                searchPlus += "+"
            else:
                break

    print(searchPlus + x)

    if searchPlus:
        r_json = API_URL + "&query=" + searchPlus  
        # return app.add_url_rule(searchPlus, 'index', index)
    
    else:
        r_json = API_URL + "&query=default"
        search = ''
    
#     print(searchPlus + x)

    if r_json:

        response = requests.get(r_json) # request.response Obj

        movies = json.loads(response.text) # into a dict
        

        print(r_json)

    
        if npage:
            print('pressed!')
            print(counter)
            counter += 2
            postcounter = counter + 4
            movies_slice = movies['results'][counter:postcounter]

        else:
            movies_slice = movies['results']

    
    
    # print(movies_slice)

    # doc = BeautifulSoup(response.text, "html.parser")
    # print(doc.title)

    # with open('templates/index.html', 'r') as p:
    #     doc = BeautifulSoup(p, 'html.parser')
    
    # result = doc.find_all('button')

    #     return render_template('index.html', urlView=r_json)


@app.route('/results')
def results():

    
#     counter = 0

#     search = request.form.get('search')
#     npage = request.form.get('npage')
    
    

    
    
#     if r_json:

#         response = requests.get(r_json) # request.response Obj
#         movies = json.loads(response.text) # into a dict

#         print(r_json)

#         if npage:
#             print('pressed!')
#             print(counter)
#             counter += 2
#             postcounter = counter + 4
#             movies_slice = movies['results'][counter:postcounter]
#         else:
#             movies_slice = movies['results']

    

    return render_template('index.html', movies=movies_slice, search=search, counter=counter)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(15), unique=True)
#     password = db.Column(db.String(80), unique=True)

#     def __repr__(self):
#         return '<User %r>' % self.id

x = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
    

if __name__ == "__main__":
    app.run(debug=True)
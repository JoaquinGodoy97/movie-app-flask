from urllib import response
from flask import Flask, flash, render_template, request, redirect, url_for, Blueprint, session
from flask_sqlalchemy import SQLAlchemy
import json, requests

home = Blueprint('home', __name__)

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
    search_split_by_plus = ""
    list_without_space = search.split() #result into a list 

    for i in range(0,len(list_without_space)):
        search_split_by_plus += str(list_without_space[i])
    
        if i < len(list_without_space) - 1:
            search_split_by_plus += "+" # adding plus symbol
        else:
            return search_split_by_plus

@home.route('/', methods=['GET', 'POST'])
def search(page = 1):
    x = "***************************************************"
    search_plus = ""
    
    search = request.form.get('search')
    
    if 'search' in request.form:
        
        if search == "":
            return redirect(url_for("home.search")) # default search

        else:
            
            search_plus = render_results(search)
            return redirect(url_for('results.search_list', search_result=search_plus, page_num=1))
    else:
        if 'npage' in request.form:
            print('pressed from home!')


    return render_template('index.html', messages=search)



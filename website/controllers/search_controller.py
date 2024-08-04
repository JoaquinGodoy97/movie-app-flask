from flask import render_template, request, Blueprint, session

homepage = Blueprint('homepage', __name__)

@homepage.route('/search', methods=['GET', 'POST']) # change the route by "/" to make it default /search
def search():
    # search_plus_formatted = ""

    from website.view import logout_redirect, homepage_search_redirect, go_to_first_page_results, render_homepage_template
    
    search = request.form.get('search') ## apparently request.form .from() creates an html form for capturing the data
    
    if request.method == 'POST':

        if request.form.get('logout') == 'Log Out':
                return logout_redirect()
            
        elif search:
            if search == "":
                return homepage_search_redirect()
            
            else:
                search_plus_formatted = reformat_search_results(search)
                return go_to_first_page_results(search_plus_formatted, current_page=1)
            
    else:
        if "username" not in session:
            return logout_redirect()

    return render_homepage_template()

def reformat_search_results(search):
    list_without_space = search.split() #result into a list 

    search_plus_formatted = "+".join(list_without_space)
    return search_plus_formatted

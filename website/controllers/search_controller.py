from flask import request, Blueprint, session
from website.services.search_services import reformat_search_results, search_results
from website.view.view import logout_redirect, homepage_search_redirect, render_homepage_template

homepage = Blueprint('homepage', __name__)

@homepage.route('/search', methods=['GET', 'POST'])
def search():
    """
    Handles homepage search submission and reformatting of search input.

    Returns:
        Response: Rendered template results with search result formatted, if failed loops homepage.
    """
    search = request.form.get('search') ## apparently request.form .from() creates an html form for capturing the data
    
    if request.method == 'POST':
        if request.form.get('logout') == 'Log Out':
            return logout_redirect()
            
        elif search:
            if search == "":
                return homepage_search_redirect()
            
            else:
                search_plus_formatted = reformat_search_results(search)
                current_service = 'results.results_search_list'
                return search_results(search_plus_formatted, 1, current_service)
            
    else:
        if "username" not in session:
            return logout_redirect()
        
    return render_homepage_template()
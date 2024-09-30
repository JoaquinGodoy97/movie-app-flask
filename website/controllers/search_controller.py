from flask import request, Blueprint, session, jsonify
from website.services.search_services import search_results
from website.view.view import logout_redirect, homepage_search_redirect, render_homepage_template
from website.utils.config import Services

homepage = Blueprint('homepage', __name__)

@homepage.route('/search', methods=['POST'])
def search():
    """
    Handles homepage search submission and reformatting of search input.

    Returns:
        Response: Rendered template results with search result formatted, if failed loops homepage.
    """

    data = request.json
    search_result = data.get('search')
    print(search_result)
    # search_result = request.args.get('query', '')
    # current_page = request.args.get('page', 1, type=int)

    if request.form.get('logout') == 'Log Out':
        return logout_redirect()

    elif search_result:
        if search_result == "":
            return homepage_search_redirect()
        
        else:
            # search_plus_formatted = reformat_search_results(search_result)
            # print(search_plus_formatted)
            current_service = Services.RESULTS_SERVICE_ENDPOINT
            # return jsonify({ "redirect": f"/{current_service}/{search_plus_formatted}/1"})
            return search_results(search_result, 1, current_service)
        
    # # If no search_result, return an error message
    return jsonify({'error': 'No search query provided'})
            
    # else:
    #     if "username" not in session:
    #         return logout_redirect()
        
    # return render_homepage_template()
from flask import request, Blueprint, session, jsonify
from server.services.search_services import search_results
from server.view.view import logout_redirect, homepage_search_redirect, render_homepage_template
from server.utils.settings import Services
from server.services.auth_services import login_required, Security


homepage = Blueprint('homepage', __name__)

@homepage.route('/search', methods=['POST'])
def search():
    """
    Handles homepage search submission and reformatting of search input.

    Returns:
        Response: Rendered template results with search result formatted, if failed loops homepage.
    """
    has_access = Security.verify_token(request.headers)

    if has_access:

        data = request.json
        search_result = data.get('search')
        # search_result = request.args.get('query', '')
        # current_page = request.args.get('page', 1, type=int)

        if request.form.get('logout') == 'Log Out':
            return logout_redirect()

        elif search_result:
            if search_result == "":
                return homepage_search_redirect()
            
            else:
                # search_plus_formatted = reformat_search_results(search_result) # Not necessary already formatted from react.
                current_service = Services.RESULTS_SERVICE_ENDPOINT
                return search_results(search_result, 1, current_service)
            
        # # If no search_result, return an error message
        return jsonify({'error': 'No search query provided'})
    else:
        return jsonify({ 'message': 'Unauthorized token.', 'redirect': '/login'}), 401
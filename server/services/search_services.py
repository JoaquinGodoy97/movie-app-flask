from flask import jsonify
from server.view.view import homepage_search_redirect, go_to_first_page_redirect
from server.utils.settings import Services
# from website.controllers.search_controller import sear


# It seems that it is not necessary since automatically transforms the "space" into "%20"
# def reformat_search_results(search):

#     """
#     Handled search text into api needed format. ex. "hello to the world" => "hello+to+the+world".

#     """
#     list_without_space = search.split() #result into a list 

#     search_plus_formatted = "+".join(list_without_space)
#     return search_plus_formatted

def search_results(search, current_page, current_service):
    # if current_service == "":
    #     current_service = 'homepage.search'

    if current_service == "":
        current_service = Services.HOMEPAGE_SERVICE_ENDPOINT

    if search == "":
        return homepage_search_redirect()
        # return jsonify({ "message": "Going backa to homepage", "redirect": "/search"})
                
    else:
        # search_plus_formatted = reformat_search_results(search)
        return go_to_first_page_redirect(search, current_page, current_service)
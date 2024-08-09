from website.view.view import homepage_search_redirect, go_to_first_page_redirect
# from website.controllers.search_controller import sear

def reformat_search_results(search):

    """
    Handled search text into api needed format. ex. "hello to the world" => "hello+to+the+world".

    """
    list_without_space = search.split() #result into a list 

    search_plus_formatted = "+".join(list_without_space)
    return search_plus_formatted

def search_results(search, current_page, current_service):
    # if current_service == "":
    #     current_service = 'homepage.search'

    if current_service == "":
        current_service = 'homepage.search'

    if search == "":
        homepage_search_redirect()
                
    else:
        search_plus_formatted = reformat_search_results(search)
        return go_to_first_page_redirect(search_plus_formatted, current_page, current_service)
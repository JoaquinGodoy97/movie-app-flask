# RESULTS_SERVICE_ENDPOINT = 'results.results_search_list'
# RESULTS_SERVICE_ENDPOINT = "results"
# HOMEPAGE_SERVICE_ENDPOINT = 'homepage.search'

class Services:
    # RESULTS_SERVICE_ENDPOINT = 'results.results_search_list'
    RESULTS_SERVICE_ENDPOINT = "results"
    HOMEPAGE_SERVICE_ENDPOINT = "homepage.search"

class Messages:
    MSG_USER_LOGGEDIN = "User already logged in"
    ERROR_MSG_PASSINVALID = 'Invalid Password'
    
    @staticmethod
    def welcome_back_user(user):
        return f"Welcome back, {user}!"


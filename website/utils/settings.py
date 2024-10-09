from decouple import config

class DevelopmentConfig():
    DEBUG = config('DEBUG')
    SQLALCHEMY_TRACK_MODIFICATIONS = config('SQLALCHEMY_TRACK_MODIFICATIONS')
    SQLALCHEMY_DATABASE_URI = config('SQLALCHEMY_DATABASE_URI')

# config = {
#     'development': DevelopmentConfig # environment //
# }

class Config():
    SECRET_KEY = config('SECRET_KEY');

API_KEY = config('API_KEY')
BASE_URL = config('BASE_URL')
API_URL = BASE_URL + '/search/movie?' + 'api_key=' + API_KEY

class Services:
    # RESULTS_SERVICE_ENDPOINT = 'results.results_search_list'
    RESULTS_SERVICE_ENDPOINT = "results"
    HOMEPAGE_SERVICE_ENDPOINT = "homepage.search"

class Messages:
    MSG_USER_LOGGEDIN = "User already logged in"
    ERROR_MSG_PASSINVALID = 'Invalid Password'
    MOVIES_NOT_FOUND = "No movies found."
    PAGE_NOT_FOUND = "Page not found."
    USER_CREATED = "User created successfuly."
    
    @staticmethod
    def welcome_back_user(user):
        return f"Welcome back, {user}!"
    
    @staticmethod
    def user_created(user, password):
        USER_CREATED = f"User '{user}' created successfuly. Don't forget your password is: {password}"    
# RESULTS_SERVICE_ENDPOINT = 'results.results_search_list'
# RESULTS_SERVICE_ENDPOINT = "results"
# HOMEPAGE_SERVICE_ENDPOINT = 'homepage.search'
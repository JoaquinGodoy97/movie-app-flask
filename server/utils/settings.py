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
FRONTEND_URL=config('FRONTEND_URL')
DB_NAME = config('DB_NAME')
FLASK_RUN_PORT = config('FLASK_RUN_PORT')
FLASK_RUN_HOST = config('FLASK_RUN_HOST')

class Services:
    # RESULTS_SERVICE_ENDPOINT = 'results.results_search_list'
    RESULTS_SERVICE_ENDPOINT = "results"
    HOMEPAGE_SERVICE_ENDPOINT = "homepage.search"

class Messages:
    MSG_USER_LOGGEDIN = "User already logged in"
    ERROR_MSG_PASSINVALID = 'Invalid Password. Write a password between 5-9 characters long no spaces.'
    ERROR_MSG_INVALIDPASSWORD = 'Invalid password.'
    ERROR_MSG_INVALIDUSERNAME_NOTREGISTERED = 'Invalid username. Write a username between 5-9 characters long no spaces.'
    ERROR_MSG_INVALIDPASS_NOTREGISTERED = 'Invalid password. Write a password between 5-9 characters long no spaces.'
    ERROR_MSG_AUTHINVALIDFORMAT = 'Invalid format. Write a username and passowrd between 5-9 characters long no spaces.'

    MOVIES_NOT_FOUND = "No movies found."
    PAGE_NOT_FOUND = "Page not found."
    USER_CREATED = "User created successfuly."
    # HOMEPAGE_REDIRECT = "User created successfuly."
    
    @staticmethod
    def welcome_back_user(user):
        return f"Welcome back, {user}!"
    
    @staticmethod
    def user_created(user, password):
        USER_CREATED = f"User '{user}' created successfuly. Don't forget your password is: {password}"    
# RESULTS_SERVICE_ENDPOINT = 'results.results_search_list'
# RESULTS_SERVICE_ENDPOINT = "results"
# HOMEPAGE_SERVICE_ENDPOINT = 'homepage.search'
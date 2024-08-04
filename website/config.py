class DevelopmentConfig():
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'

config = {
    'development': DevelopmentConfig
}

API_KEY = 'api_key=52495a0d2fceefe863149757f96d5d21'
BASE_URL = 'https://api.themoviedb.org/3'
API_URL = BASE_URL + '/search/movie?' + API_KEY

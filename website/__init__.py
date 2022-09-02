from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SECRET_KEY']= "milanesa"
    
    from .results import results
    from .home import home

    app.register_blueprint(results, url_prefix="/") #all of the url store inside how do I access
    app.register_blueprint(home, url_prefix="/") #all of the url store inside how do I access

    return app
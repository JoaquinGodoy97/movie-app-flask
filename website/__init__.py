from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def create_app():

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:passwordtest123@localhost/moviewishlist'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY']= "milanesa"

    SQLAlchemy(app)
    
    from .results import results
    from .home import home
    from .registration import registration

    app.register_blueprint(results, url_prefix="/") #all of the url store inside how do I access
    app.register_blueprint(home, url_prefix="/") #all of the url store inside how do I access
    app.register_blueprint(registration, url_prefix="/") #all of the url store inside how do I access

    return app
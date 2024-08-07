from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from website.utils.db import db, DB_NAME
from os import path #operating system
from flask_migrate import Migrate

migrate = Migrate()

def create_app():

    app = Flask(__name__)
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:passwordtest123@localhost/moviewishlist'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY']= "milanesa"

    # SQLAlchemy(app)
    # Initialize the SQLAlchemy instance with the app
    db.init_app(app)
    migrate.init_app(app, db) #update DB location

    from .controllers.wishlist_controller import wishlist
    from .controllers.search_controller import homepage
    from .controllers.results_controller import results
    from .controllers.auth_controller import auth

    app.register_blueprint(wishlist, url_prefix="/")
    app.register_blueprint(results, url_prefix="/") #all of the url store inside how do I access
    app.register_blueprint(homepage, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    
    app.secret_key = 'your_secret_key'
    # from website.models.user import User

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

if __name__ == "__main__":
        app = Flask(__name__)
        create_database(app)
        app.run()
#---------------------------------------------------------------------------

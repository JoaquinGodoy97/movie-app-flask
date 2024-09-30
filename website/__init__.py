from flask import Flask, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from website.utils.db import db, DB_NAME
from os import path #operating system
from flask_migrate import Migrate
from website.view.view import render_page_not_found
import logging
from flask_cors import CORS

migrate = Migrate()

def create_app():

    app = Flask(__name__, static_folder='../client/public', static_url_path='')
    
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": "http://localhost:3000"}})

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY']= "milanesa"

    # Initialize the SQLAlchemy instance with the app
    db.init_app(app)
    migrate.init_app(app, db) # Update DB location

    from .controllers.wishlist_controller import wishlist
    from .controllers.search_controller import homepage
    from .controllers.results_controller import results
    from .controllers.auth_controller import auth

    app.register_blueprint(wishlist, url_prefix="/")
    app.register_blueprint(results, url_prefix="/")
    app.register_blueprint(homepage, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    @app.route('/')
    def serve():
        return send_from_directory(app.static_folder, 'index.html')

    @app.route('/<path:path>')
    def serve_static(path):
        return send_from_directory(app.static_folder, path)
    
    @app.route('/css/<path:filename>')
    def serve_css(filename):
        return send_from_directory(app.static_folder, filename)

    @app.errorhandler(404)
    def page_not_found(e):
        return send_from_directory(app.static_folder, 'index.html')
    
    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():  # Ensure app context is available
            db.create_all()
        print('Created Database!')

if __name__ == "__main__":
    app = create_app()
    create_database(app)
    app.run()



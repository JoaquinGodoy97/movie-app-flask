from flask import Flask, send_from_directory
from server.utils.db import db
from server.utils.settings import FRONTEND_URL, Config, DB_NAME
from os import path
from flask_migrate import Migrate
from flask_cors import CORS
from server.utils.db_pool import create_users_table

migrate = Migrate()

def create_app():

    app = Flask(__name__, static_folder='../client/public', static_url_path='')
    
    # Allow CORS from local and production frontends 
    print(f"Loaded FRONTEND_URL: {FRONTEND_URL}")
    # frontend_url = environ.get('FRONTEND_URL', 'http://localhost:3000')
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": FRONTEND_URL}})

    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY']=Config.SECRET_KEY
    
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

# def create_database(app):
#     if not path.exists('server/' + DB_NAME):
#         with app.app_context():  # Ensure app context is available
#             # db.create_all()
#             create_users_table()
#         print('Created Database!')

# if __name__ == "__main__":
#     app = create_app()
#     create_database(app)
#     app.run()



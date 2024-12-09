from server.utils.db import db
from models.user_model import User

def add_user_to_db(user, email, password):
    """
    Adds user to the database.

    Args:
        user (str): The search query. No restrictions yet.
        email (int): The current page number. Optional, not functional yet.
        password (str): The name of the movie. 5-9 characters long no spaces and contain only alphanumeric characters.

    Returns:
        Response: Rendered template with the updated results.
    """
    print(user, password)
    try:
        
        user_db = User(user, email, password)
        db.session.add(user_db)
        db.session.commit()

        # password_reminder_alert(user, password) # routing alert // business logic
        # return homepage_search_redirect()
    
    except Exception as e:
        db.session.rollback()
        # database_save_error_alert(e)
        print('failed to create user')

    # finally:
    #     close_session()


def user_query_filter_by_name(user):
    found_user = User.query.filter_by(username=user).first() # modificar
    return found_user
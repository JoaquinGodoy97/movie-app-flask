from website.config import BASE_URL, API_KEY
from flask import request
from website.utils.db import db
from website.models.wishlist_user_model import Wishlist_user
from website.view.view import database_save_error_alert, database_wishlist_delete_erorr_alert, database_delete_error_alert
import requests, re

def get_results_by_movie_id(results):
        for movie in results:
                api_url = BASE_URL + "/movie/" + str(movie.mv_id) + "?" + API_KEY
                
                response = requests.get(api_url)
                response.raise_for_status()  # Check for HTTP request errors
                results_json = response.json()

                # Update movie_data fields
                movie.title = results_json.get('title')
                movie.poster_path = results_json.get('poster_path')
                movie.overview = results_json.get('overview')
        return results

def filter_by_usersession_and_movieid(user_session, movie_id):
        return Wishlist_user.query.filter_by(user_id=user_session, mv_id=movie_id).first()

def filter_by_usersession(user_session):
        return Wishlist_user.query.filter_by(user_id=user_session).all()

def add_to_wishlist_db(movie_id, movie_name, user_id):
        try:
                user_data = Wishlist_user(mv_id=movie_id, title=movie_name, user_id=user_id)
                db.session.add(user_data)
                db.session.commit()

        except Exception as e:
                db.session.rollback()
                database_save_error_alert(e)

        finally:
                db.session.close()

def remove_from_wishlist_db(found_movie_to_delete):
        try:
                db.session.delete(found_movie_to_delete)
                db.session.commit()
                database_wishlist_delete_erorr_alert(found_movie_to_delete.title, found_movie_to_delete.mv_id)

        except Exception as e:
                db.session.rollback()
                database_delete_error_alert(e)
        finally:
                db.session.close()

def filter_movies_by_search_if_any(movies, search_result):
        if search_result:
                pattern = re.compile(f".*?{re.escape(search_result)}.*?", re.IGNORECASE)
                filtered_movies = filter(lambda movie: pattern.search(movie.title), movies)
                return list(filtered_movies)
        return movies
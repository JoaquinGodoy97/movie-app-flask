from server.utils.settings import BASE_URL, API_KEY
from flask import request, session, jsonify
from server.utils.db import db
from server.models.wishlist_user_model import Wishlist_user
from server.view.view import database_save_error_alert, database_wishlist_delete_erorr_alert, database_delete_error_alert
import requests, re


def get_results_by_movie_id(results):
        updated_results = [] 

        for movie in results:
                api_url = BASE_URL + "/movie/" + str(movie['mv_id']) + "?api_key=" + API_KEY
                
                response = requests.get(api_url)
                response.raise_for_status()  # Check for HTTP request errors
                results_json = response.json()

                # print(results_json)

                updated_movie = {
                'id': movie['id'],
                'mv_id': movie['mv_id'],
                'username': movie['username'],
                'title': results_json.get('title', movie['title']),  # Use existing title if not found
                'poster_path': results_json.get('poster_path', None),
                'overview': results_json.get('overview', None),
                }

                updated_results.append(updated_movie)

        return updated_results

def filter_by_usersession_and_movieid(user, movie_id):
        return Wishlist_user.query.filter_by(username=user, mv_id=movie_id).first()

def filter_by_usersession(username):
        
        movies = Wishlist_user.query.filter_by(username=username).all()
        return [movie_to_dict(movie) for movie in movies]

def bring_single_movie_by_user(user, movie_id):
        return Wishlist_user.query.filter_by(username=user, mv_id=movie_id).first() is not None

def movie_to_dict(movie):
        return {
                'id': movie.id,
                'mv_id': movie.mv_id,
                'title': movie.title,
                'username': movie.username # change the front end
        }

def add_to_wishlist_db(movie_id, movie_name, username):

        try:
                user_data = Wishlist_user(mv_id=movie_id, title=movie_name, username=username)

                db.session.add(user_data)
                db.session.commit()

        except Exception as e:
                db.session.rollback()
                database_save_error_alert(e)

        finally:
                db.session.close()

def is_wishlist_user_limit_reached(user):
        list = Wishlist_user.query.filter_by(username=user).all()
        list_length = len(list)
        return list_length >= 50

def remove_from_wishlist_db(found_movie_to_delete):
        try:
                db.session.delete(found_movie_to_delete)
                db.session.commit()
                database_wishlist_delete_erorr_alert(found_movie_to_delete.title, found_movie_to_delete.mv_id)
                return jsonify({ "message": "Movie removed successfuly", "method": 'remove'})

        except Exception as e:
                db.session.rollback()
                database_delete_error_alert(e)
        finally:
                db.session.close()

def filter_movies_by_search_if_any(movies, search_result):
        if search_result:
                pattern = re.compile(f".*?{re.escape(search_result)}.*?", re.IGNORECASE)
                filtered_movies = filter(lambda movie: pattern.search(movie['title']), movies)

                return list(filtered_movies)
        return movies

def bring_multiple_movies_by_user(user, movie_ids):
        # Assuming you have a User and a Wishlist model
        # Query the wishlist table for this user and the provided movie IDs
        wishlist_items = Wishlist_user.query.filter(Wishlist_user.username == user, Wishlist_user.mv_id.in_(movie_ids)).all()
        # Create a dictionary with movie_id as keys and True/False as values
        wishlist_statuses = {mv_id: False for mv_id in movie_ids}  # Initialize all to False
        
        for item in wishlist_items:
                wishlist_statuses[item.mv_id] = True  # Set to True for movies in the wishlist
        
        return wishlist_statuses
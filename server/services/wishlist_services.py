from server.utils.settings import BASE_URL, API_KEY
import requests, re
from server.utils.db_connection import get_db_connection
from mysql import connector

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

def movie_to_dict(movie):
        print("PRINTING MOVIE: ", movie)
        return {
                'id': movie.id,
                'mv_id': movie.mv_id,
                'title': movie.title,
                'username': movie.username # change the front end
        }

def is_wishlist_user_limit_reached(username):
        list = filer_movies_by_username(username)
        list_length = len(list)
        return list_length >= 50

def filter_movies_by_search_if_any(movies, search_result):
        if search_result:
                pattern = re.compile(f".*?{re.escape(search_result)}.*?", re.IGNORECASE)
                filtered_movies = filter(lambda movie: pattern.search(movie['title']), movies)

                return list(filtered_movies)
        return movies

def filter_by_usersession(username):
        
        movies = filer_movies_by_username(username)
        # return [movie_to_dict(movie) for movie in movies] # Apparently not needed with Mysql
        return movies

def bring_multiple_movies_by_user(user, movie_ids):
        # Assuming you have a User and a Wishlist model
        # Query the wishlist table for this user and the provided movie IDs
        wishlist_items = bring_movies_by_user_and_movie_id(user, movie_ids)
        # Create a dictionary with movie_id as keys and True/False as values
        wishlist_statuses = {mv_id: False for mv_id in movie_ids}  # Initialize all to False
        
        for item in wishlist_items:
                wishlist_statuses[item['mv_id']] = True  # Set to True for movies in the wishlist
        
        return wishlist_statuses


"""
DB SERVICES
"""

# def add_to_wishlist_db(movie_id, movie_name, username):

#         try:
#                 user_data = Wishlist_user(mv_id=movie_id, title=movie_name, username=username)

#                 db.session.add(user_data)
#                 db.session.commit()

#         except Exception as e:
#                 db.session.rollback()
#         finally:
#                 db.session.close()

def add_to_wishlist_db(movie_id, movie_name, username):
        query = "INSERT INTO wishlist_user (mv_id, title, username) VALUES (%s, %s, %s)"
        try:
                connection = get_db_connection()
                cursor = connection.cursor()
                cursor.execute(query, (movie_id, movie_name, username))
                connection.commit()
                print("Wishlist user added successfully.")
        except connector.Error as e:
                print(f"Error adding wishlist user: {e}")
                connection.rollback()
        finally:
                cursor.close()
                connection.close()


# def remove_from_wishlist_db(found_movie_to_delete):
#         try:
#                 db.session.delete(found_movie_to_delete)
#                 db.session.commit()
#                 return movie_removed_success()

#         except Exception as e:
#                 db.session.rollback()
#         finally:
#                 db.session.close()

def remove_from_wishlist_db(movie_id):
        query = """
                DELETE FROM wishlist_user 
                WHERE mv_id = %s
                """
        try:
                connection = get_db_connection()
                cursor = connection.cursor()
                cursor.execute(query, (movie_id,))
                connection.commit()
                print("Wishlist movie removed successfully.")
        except Exception as e:
                print(f"Error removing movie: {e}")
        finally:
                cursor.close()
                connection.close()

# def filer_movies_by_username(username):
#         return Wishlist_user.query.filter_by(username=username).all()

def filer_movies_by_username(username):
        query = "SELECT * FROM wishlist_user WHERE username = %s"

        try:
                connection = get_db_connection()
                cursor = connection.cursor(dictionary=True)
                cursor.execute(query, (username,))
                username = cursor.fetchall()
                
                return username
        except connector.Error as e:
                print(f"Error bringing username from Wishlist db: {e}")
        finally:
                cursor.close()
                connection.close()

# def filter_by_usersession_and_movieid(user, movie_id):
#         return Wishlist_user.query.filter_by(username=user, mv_id=movie_id).first()

def filter_by_usersession_and_movieid(user, movie_id):
        query = """
                SELECT * 
                FROM wishlist_user
                WHERE username = %s AND mv_id = %s
                LIMIT 1
        """

        try:
                connection = get_db_connection()
                cursor = connection.cursor()
                cursor.execute(query, (user, movie_id))
                result = cursor.fetchone()
                return result
        except connector.Error as e:
                print(f"Error filtering wishlist: {e}")
                return None
        finally:
                cursor.close()
                connection.close()

# def bring_single_movie_by_user(user, movie_id):
#         return Wishlist_user.query.filter_by(username=user, mv_id=movie_id).first() is not None

def bring_single_movie_by_user(user, movie_id):
        query = """
                SELECT 1 
                FROM wishlist_user
                WHERE username = %s AND mv_id = %s
                LIMIT 1
        """

        try:
                connection = get_db_connection()
                cursor = connection.cursor(dictionary=True)
                cursor.execute(query, (user, movie_id))
                result = cursor.fetchone()
                return result is not None
        except connector.Error as e:
                print(f"Error checking single movie: {e}")
                return None
        finally:
                cursor.close()
                connection.close()

# def bring_movies_by_user_and_movie_id(user, movie_ids):
#         return Wishlist_user.query.filter(Wishlist_user.username == user, Wishlist_user.mv_id.in_(movie_ids)).all()

def bring_movies_by_user_and_movie_id(user: str, movie_ids: list):
        placeholders = ', '.join(['%s'] * len(movie_ids))
        query = f"""
                SELECT *
                FROM wishlist_user
                WHERE username = %s AND mv_id IN ({placeholders})
        """

        try:
                connection = get_db_connection()
                cursor = connection.cursor(dictionary=True)
                cursor.execute(query, [user] + movie_ids )
                results = cursor.fetchall()
                return results
        except connector.Error as e:
                print(f"Error bringin movies: {e}")
                return []
        finally:
                cursor.close()
                connection.close()

# Wishlist_user.query.filter_by(mv_id=movie_id).first()

def wishlist_filter_query_by_movie_id(movie_id):
        query = "SELECT * FROM wishlist_user WHERE mv_id = %s"

        try:
                connection = get_db_connection()
                cursor = connection.cursor()
                cursor.execute(query, (movie_id,))
                movie = cursor.fetchone()
                return movie
        except Exception as e:
                print(f"Error finding movie by id: {e}")
        finally:
                cursor.close()
                connection.close()


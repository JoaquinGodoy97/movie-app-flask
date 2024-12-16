from flask import session, jsonify
from server.models.user_model import User
from functools import wraps
import jwt 
from datetime import datetime, timedelta, timezone
from decouple import config
from server.utils.db_connection import get_db_connection
from server.utils.settings import SUPER_ADMIN_USERNAME
from mysql import connector
# from app import ap

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return jsonify({'error': 'Unauthorized decorator', 'redirect': '/login'}), 401
        return f(*args, **kwargs)
    return decorated_function

class Security():
    secret = config('JWT_KEY')

    @classmethod
    def generate_token(cls, authenticated_user):
        payload = {
            "iat": datetime.now(timezone.utc),
            'exp': datetime.now(timezone.utc) + timedelta(minutes=20),
            'username': authenticated_user.username
        }
        return jwt.encode(payload, cls.secret, algorithm="HS256")
    
    @classmethod
    def verify_token(cls, headers):
        if 'Authorization' in headers.keys():
            authorization = headers['Authorization']
            jwt_payload = authorization.split(" ")[1]
            # print("JWT Payload:", jwt_payload)
            
            try:
                return jwt.decode(jwt_payload, cls.secret, algorithms=["HS256"])
            except jwt.ExpiredSignatureError:
                print("Error: The token has expired")
                return False
            except (jwt.DecodeError, jwt.InvalidTokenError):
                print("Error: Invalid token")
                return False
            except jwt.InvalidIssuerError:
                print("Error: Invalid issuer")
                return False
        return False


def open_session(user):
    session['username'] = user
    session['loggged_in'] = True

def close_session():
    session.pop('username', None)

def close_session():
    session.pop('username', None)

def is_user_logged_in(session):
    return 'username' in session

def validate_credentials(username, password):
    """Helper function to validate username and password."""
    validated_user = User.validate_user(username)
    validated_password = User.validate_password(password)
    return validated_user, validated_password

def user_to_dict(user):
    return {
        "username": user.username,
        "id": user.id,
        # Add more fields as needed
    }


def add_user_to_db(username: str, password: str, email="", is_admin=False):
    query = "INSERT INTO users (username, email, password, is_admin) VALUES ( %s, %s, %s, %s)"

    email = email if email else None
    
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(query, (username, email, password, is_admin))
        connection.commit()
        print("User added successfully.")
    except connector.Error as e:
        print(f"Error adding user: {e}")
        connection.rollback()
        close_session() # Not REAlly Sure
    finally:
        cursor.close()
        connection.close()

def user_query_filter_by_name(username):
    query = "SELECT * FROM users WHERE username = %s"

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(query, (username,))
        found_user = cursor.fetchone()

        if found_user and found_user[1] == SUPER_ADMIN_USERNAME and found_user[4] == 0: # In case admin rights were not given
            update_super_admin_rights(found_user[1]) # Turning admin rights True
        elif found_user:
            instanced_user = User(found_user[0], found_user[1], found_user[2], found_user[3], found_user[4]) # ID, User, Email, Pass, admin rights
            return instanced_user
        else:
            return None
        
    except connector.Error as e:
        print(f"Error finding user: {e}")
    finally:
        cursor.close()
        connection.close()

def update_super_admin_rights(username):

    update_query = """
        UPDATE users 
        SET is_admin = TRUE 
        WHERE username = %s;
        """
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(update_query, (username,))
        connection.commit()
        print("Admin privileges updated successfuly.")
    except:
        print("Could not add super admin privileges.")
    finally:
        cursor.close()
        connection.close()

def user_query_all_users():
    query = "SELECT * FROM users;"

    users_list = []

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        found_users = cursor.fetchall()

        for user in found_users:
            instanced_user = User(user[0], user[1], user[2], user[3], user[4])  # ID, User, Email, Pass, admin rights

            users_list.append({
                "id": instanced_user.id,
                "username": instanced_user.username,
                "email": instanced_user.email,
                "password": instanced_user.password,
                "adminStatus": instanced_user.admin_status

            })
        
        return users_list
    
    except:
        print("Coul not bring list of users")
        return None
    finally:
        cursor.close()
        connection.close()

def delete_user_by_user_id(user_id):

    username = get_username_by_id(user_id)

    if not username: 
        print(f"User with ID {user_id} not found.") 
        return

    query = """
        DELETE FROM wishlist_user
        WHERE username = %s"""

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(query, (username,))
        connection.commit()
        print(f"Movies from {user_id} were deleted correctly.")
    except Exception as e:
        print("Failed to delete user:", e)
        return None
    finally:
        cursor.close()
        connection.close()
    
    return delete_empty_users(user_id)

def delete_empty_users(user_id):
    query = """
            DELETE FROM users
            WHERE id = %s"""
        
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(query, (user_id,))
        connection.commit()
        print(f"User id {user_id} deleted correctly.")

        return jsonify({"message": f"User {user_id} deleted."}), 200
    except:
        print("Failed to delete user")
        return jsonify({ "message": f"The user {user_id} have movies saved. Would you like to delete it anyways?"}), 206
        
    finally:
        cursor.close()
        connection.close()

def is_user_in_db_by_user_id(user_id):
    query = "SELECT * FROM users WHERE id = %s"

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(query, (user_id,))
        found_user = cursor.fetchone()

        if found_user:
            return True
        else:
            return False
        
    except connector.Error as e:
        print(f"Could not find user: {e}")
    finally:
        cursor.close()
        connection.close()

def update_admin_rights_with_id(user_id):
        update_admin_status = "TRUE" if get_admin_status_by_id(user_id) else 'FALSE'

        update_query = f"""
        UPDATE users 
        SET is_admin =  {update_admin_status}
        WHERE username = %s;
        """

        try:
            connection = get_db_connection()
            cursor = connection.cursor()
            cursor.execute(update_query, (user_id,))
            found_user = cursor.fetchone()
            admin_status = found_user[4]

            return admin_status
        except:
            print("Coul not update admin status.")
            return None
        finally:
            cursor.close()
            connection.close()


def get_admin_status_by_id(user_id):
    query = "SELECT * FROM users WHERE id = %s;"

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(query, (user_id,))
        found_user = cursor.fetchone()
        admin_status = found_user[4]

        print("GET ADMIN STATUS IT SHOULDNT BE 1", admin_status)
        return admin_status
    
    except:
        print("Coul not bring admin status.")
        return None
    finally:
        cursor.close()
        connection.close()

def get_username_by_id(user_id):
    query = "SELECT * FROM users WHERE id = %s;"

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(query, (user_id,))
        found_user = cursor.fetchone()
        username = found_user[1]

        return username
    
    except:
        print("Coul not bring username.")
        return None
    finally:
        cursor.close()
        connection.close()
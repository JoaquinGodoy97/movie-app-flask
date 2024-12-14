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

        if found_user and found_user[1] == SUPER_ADMIN_USERNAME and found_user[4] == False: 
            update_super_admin_rights(found_user[1])
        elif found_user:
            instanced_user = User(found_user[1], found_user[2], found_user[3], found_user[4]) # User, Email, Pass
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
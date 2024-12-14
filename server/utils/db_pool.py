from mysql.connector import connect
from server.utils.settings import FLASK_RUN_HOST
from server.services.auth_services import add_user_to_db, user_query_filter_by_name
from server.utils.settings import SUPER_ADMIN_PASSWORD, SUPER_ADMIN_USERNAME
from server.utils.db_connection import get_db_connection

def create_database():

    try:
        connection = connect(
            host='localhost',
            user="root",
            password="root"
        )
        
        cursor = connection.cursor()
        cursor.execute("SHOW DATABASES LIKE 'movies_db';")
        result = cursor.fetchone()

        if not result:  
            cursor.execute("CREATE DATABASE movies_db;")
            connection.commit()
            print('Created database `movies_db`.')
        else:
            print('Database `movies_db` already exists.')
    except Exception as e:
        print(f"Error creating database: {e}")
    finally:
        cursor.close()
        connection.close()

def create_users_table():

    create_users_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(10) NOT NULL UNIQUE,
        email VARCHAR(30),
        password VARCHAR(10) NOT NULL,
        is_admin BOOLEAN DEFAULT FALSE
    );
    """

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES LIKE 'users';")
        result = cursor.fetchone()
        if not result:
            cursor.execute(create_users_table_query)
            connection.commit()
            print("Table users created successfully.")
            initialize_super_admin()
        else:
            print("Table users already exists.")
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        cursor.close()
        connection.close()

def create_wishlist_user_table():

    create_wishlist_user_table = """
    CREATE TABLE IF NOT EXISTS wishlist_user (
        id	INT AUTO_INCREMENT PRIMARY KEY,
        mv_id	INT NOT NULL,
        title	VARCHAR(150) NOT NULL,
        username	VARCHAR(10) NOT NULL,
	    CONSTRAINT fk_wishlist_user_username_user FOREIGN KEY(username) REFERENCES users (username)
    );
    """

    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES LIKE 'users';")
        result = cursor.fetchone()
        if not result:
            cursor.execute(create_wishlist_user_table)
            connection.commit()
            print("Table wishlist_user created successfully.")
        else:
            print("Table wishlist_user already exists.")
    except Exception as e:
        print(f"Error creating table: {e}")
    finally:
        cursor.close()
        connection.close()

def initialize_super_admin():

    if not SUPER_ADMIN_USERNAME or not SUPER_ADMIN_PASSWORD:
        raise Exception('Super admin credentials are not set in environment variables.')
    
    super_admin = user_query_filter_by_name(SUPER_ADMIN_USERNAME)

    if not super_admin:
        add_user_to_db(SUPER_ADMIN_USERNAME, SUPER_ADMIN_PASSWORD, None, True)
        print("Super admin created.")
    else:
        print("Super admin already in DB.")


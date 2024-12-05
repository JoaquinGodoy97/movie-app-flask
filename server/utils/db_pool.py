from mysql.connector import pooling, connect
from server.utils.settings import FLASK_RUN_HOST

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
        password VARCHAR(10) NOT NULL
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

def init_connection_pool():
    connection_pool = pooling.MySQLConnectionPool(
        pool_name='apimovies-pool',
        pool_size=5,
        host='localhost',
        user="root",
        password="root",
        database="movies_db"
    )
    return connection_pool

def get_db_connection():
    connection_pool = init_connection_pool()
    return connection_pool.get_connection()
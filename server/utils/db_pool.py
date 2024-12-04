from mysql.connector import pooling, connect
from server.utils.settings import FLASK_RUN_HOST



# Function to create the database if it doesn't exist
def create_database():

    connection = connect(
        host='localhost',
        user="root",
        password="root"
    )
    # First, check if the database exists
    cursor = connection.cursor()
    cursor.execute("SHOW DATABASES LIKE 'movies_db';")
    result = cursor.fetchone()

    if not result:  # If the database doesn't exist, create it
        cursor.execute("CREATE DATABASE movies_db;")
        connection.commit()
        print('Created database `movies_db`.')
    else:
        print('Database `movies_db` already exists.')

    cursor.close()
    connection.close()

def create_users_table():

    # Define the table creation query
    create_table_query = """
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
        cursor.execute(create_table_query)
        connection.commit()
        print("Table `users` created successfully.")
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
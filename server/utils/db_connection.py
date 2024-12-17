from mysql.connector import pooling
from server.utils.settings import DB_USER, DB_HOST, DB_NAME ,DB_PASSWORD

connection_pool = None

def initialize_connection_pool():
    global connection_pool
    connection_pool = pooling.MySQLConnectionPool(
        pool_name='apimovies-pool',
        pool_size=5,
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

def get_db_connection():
    if connection_pool is None: 
        initialize_connection_pool()
    return connection_pool.get_connection()

from mysql.connector import pooling

connection_pool = pooling.MySQLConnectionPool(
    pool_name='apimovies-pool',
    pool_size=5,
    host='localhost',
    user="root",
    password="root",
    database="movies_db"
)

def get_db_connection():
    return connection_pool.get_connection()

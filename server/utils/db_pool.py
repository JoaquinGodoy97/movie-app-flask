from mysql.connector import pooling
from server.utils.settings import FLASK_RUN_HOST

connection_pool = pooling.MySQLConnectionPool(
    pool_name='mypool',
    pool_size=5,
    host='localhost',
    user="root",
    password="password",
    database="database"
)

def get_db_connection():
    return connection_pool.get_connection()

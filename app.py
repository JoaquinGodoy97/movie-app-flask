from server import create_app
from server.utils.db import db
from server.utils.db_pool import create_users_table, create_database

app = create_app()

# with app.app_context():
#     from server.utils.db import db
#     db.create_all()
create_database()
create_users_table()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
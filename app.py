from website import create_app
from website.utils.db import db

app = create_app()

with app.app_context():
    from website.utils.db import db
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
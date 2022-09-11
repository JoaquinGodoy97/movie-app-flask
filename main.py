from website import create_app
from website.utils.db import db

app = create_app()

with app.app_context():  #this creates tables when the app starts
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
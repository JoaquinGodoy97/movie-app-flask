import re

class User:
    # User(id, username, email, password):
        # id = db.Column(db.Integer, primary_key=True)
        # username = db.Column(db.String(10), unique=True, nullable=False)
        # email = db.Column(db.String(30), unique=False, nullable=True)
        # password = db.Column(db.String(20))
        # wishlist_user = db.relationship('Wishlist_user', backref='user_wishlist_username', lazy=True)


    def __init__(self, id, username, email, password, admin_status, user_plan):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.admin_status = admin_status
        self.user_plan = user_plan
        
    @staticmethod
    def validate_password(password):

        print("Password from inside validation:", password)
        password_check = r"^[A-Za-z0-9]{5,9}$"

        if re.match(password_check, password):
            return True
        return False
    
    @staticmethod
    def validate_user(user):
        user_check = r"^[A-Za-z0-9]{5,9}$"
        if re.match(user_check, user):
            return True
        return False
    
    def compare_password(self, password):
        return self.password == password

    def compare_user(self, user):
        return self.username == user

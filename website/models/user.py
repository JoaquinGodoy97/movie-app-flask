from re import fullmatch
from utils.db import db

class UserWishList(db.Model):
    id = db.Column(db.Integer, primary_keys=True)
    fullname = db.Column(db.String(100))
    email = db.Column(db.String(100))

    #how to add lists

    def __init__(self, fullname, email):
        self.fullname = fullname
        self.email = email
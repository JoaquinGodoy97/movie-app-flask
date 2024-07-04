from website.utils.db import db
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=False, nullable=True)
    password = db.Column(db.String(100))

    #how to add lists

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

# ----------------------------------------------------------- another way of declaring models
# class User(db.Model):
#     __tablename__ = "user"

#     id = mapped_column(Integer, primary_key=True)
#     name = mapped_column(String(15), nullable=False)
#     email = mapped_column(String(100))
#     password = mapped_column(String(50), nullable=False)
    
#     # username = db.Column(db.String(100), unique=True, nullable=False)
#     # email = db.Column(db.String(150), unique=True, nullable=False)
#     # password = db.Column(db.String(100))

#     #how to add lists

#     def __init__(self, username, email, password):
#         self.username = username
#         self.email = email
#         self.password = password
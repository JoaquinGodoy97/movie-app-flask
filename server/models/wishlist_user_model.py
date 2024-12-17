from server.utils.db import db
# from sqlalchemy.orm import Mapped
# from sqlalchemy.orm import mapped_column


class Wishlist_user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mv_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(15), db.ForeignKey('user.username'), nullable=False)
    # IMPORTANT USER ID WAS WRONGLY NAME AS ID, WHEN ITS ACUTALLY A USERNAME


    def __init__(self, mv_id ,title, username):
        self.mv_id = mv_id
        self.title = title
        self.username = username

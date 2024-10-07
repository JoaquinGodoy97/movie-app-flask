from website.utils.db import db
# from sqlalchemy.orm import Mapped
# from sqlalchemy.orm import mapped_column


class Wishlist_user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mv_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(15), db.ForeignKey('user.username'), nullable=False)
    # IMPORTANT USER ID IS WRONGLY NAME AS ID, WHEN ITS ACUTALLY A USERNAME

    #how to add lists

    def __init__(self, mv_id ,title, username):
        self.mv_id = mv_id
        self.title = title
        self.username = username
        # self.search_results = ""

    # def filter_movies_by_search_if_any(self, movie_list, search_result):
    #     if search_result:
    #         pattern = re.compile(f".*?{re.escape(search_result)}.*?", re.IGNORECASE)
    #         matches = [movie for movie in movie_list if pattern.search(movie.get('title'))]
    #         return matches
    #     else:
    #         return movie_list
from website.utils.db import db
# from sqlalchemy.orm import Mapped
# from sqlalchemy.orm import mapped_column


class Wishlist_user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mv_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    #how to add lists

    def __init__(self, mv_id ,title, user_id):
        self.mv_id = mv_id
        self.title = title
        self.user_id = user_id
        self.search_results = ""


         
        
    # def filter_movies_by_search_if_any(self, movie_list, search_result):
    #     if search_result:
    #         pattern = re.compile(f".*?{re.escape(search_result)}.*?", re.IGNORECASE)
    #         matches = [movie for movie in movie_list if pattern.search(movie.get('title'))]
    #         return matches
    #     else:
    #         return movie_list
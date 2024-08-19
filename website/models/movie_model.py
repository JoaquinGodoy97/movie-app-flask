from website.view.view import page_not_found_warning, page_not_found_wishlist_warning

class Movies:
    def __init__(self, movie_list):
        self.movies = movie_list
        self.movies_per_page = self.paginate_movies()
        self.total_pages = len(self.movies_per_page)
        
    def paginate_movies(self, items_per_page=5): 
        movie_set_list = []

        for movie_set in range(0, len(self.movies), items_per_page):
            movie_set_end = movie_set + items_per_page
            movie_set_list.append(self.movies[movie_set:movie_set_end])
        
        return movie_set_list

    def get_movies_by_page(self, current_page, current_service):
        if 1 <= current_page <= self.total_pages:
            return self.movies_per_page[current_page - 1]
        else:
            if current_service == "wishlist":
                return page_not_found_wishlist_warning()
            return page_not_found_warning()
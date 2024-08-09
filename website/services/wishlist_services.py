from website.config import BASE_URL, API_KEY
import requests

def get_results_by_movie_id(results):
        for movie in results:
                api_url = BASE_URL + "/movie/" + str(movie.mv_id) + "?" + API_KEY
                
                response = requests.get(api_url)
                response.raise_for_status()  # Check for HTTP request errors
                results_json = response.json()
                
                # Update movie_data fields
                movie.title = results_json.get('title')
                movie.poster_path = results_json.get('poster_path')
                movie.overview = results_json.get('overview')
        return results
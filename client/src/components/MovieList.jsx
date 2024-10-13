import MovieCard from "./MovieCard"

export const MovieList = ({ movies = [], loading, onWishlist, itsOnWishlist }) => {

    if (loading) {
      return (
        <div className="movielist-notfound-container">
          <h3>Loading...</h3>
          <img
            style={{ maxWidth: '50%', maxHeight: '50%' }}
            src={`${process.env.PUBLIC_URL}/loadingDuck.png`}
            alt="Loading"
          />
        </div>
      );
    }

    // HANDLING LOADING PAGE
  
    if (!movies || movies.length === null || movies.length <= 0) {

      return (
        <div className="movielist-notfound-container">
          <h3><i>Search not found</i></h3>
          
          <img className="img-duck"
            style={{ maxWidth: '50%', maxHeight: '50%' }}
            src={`${process.env.PUBLIC_URL}/loadingDuck.png`}
            alt="No movies available"
          />
          <span className="cuak!"><i>cuak!</i></span>
        </div>
      );
      
    } else {
      return (
        <div className="movie-list">
          {movies.map((movie) => (
            <MovieCard key={movie.mv_id} movie={movie} onWishlist={onWishlist} itsOnWishlist={itsOnWishlist}/>
          ))}
        </div>
      );
    }
  }
  
import MovieCard from "./MovieCard"

const MovieList = ({ movies = []}) => {
  return (
    <div className="movie-list d-flex justify-content-evenly container">

      {movies.map((movie) => 
        <MovieCard key={movie.id} movie={movie} />
      )}

    </div>
  )
}

export default MovieList;
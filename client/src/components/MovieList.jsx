import MovieCard from "./MovieCard"

export const MovieList = ({ movies = [], loading }) => {

  const handleMovies = (moviesSet) => {

    if (loading) {
      return (
        <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', height: '70vh' }}>
          <h3>Loading...</h3>
          <img
            style={{ maxWidth: '50%', maxHeight: '50%' }}
            src="https://media.istockphoto.com/id/1269500670/vector/yellow-rubber-duck-icon.jpg?s=612x612&w=0&k=20&c=xO1K6beBtVaheYpgElZcWxHD0otQDD23nV9FTCQkISo="
            alt="Loading"
          />
        </div>
      );
    }

    if (moviesSet.length > 0) {
      return moviesSet.map((movie) =>
        <MovieCard key={movie.id} movie={movie} />
      )
    }

    else {
      return (
        <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', height: '70vh' }}>
          <h3> <i>Search not found</i> </h3>
          <img
            style={{ maxWidth: '50%', maxHeight: '50%' }}
            src="https://media.istockphoto.com/id/1269500670/vector/yellow-rubber-duck-icon.jpg?s=612x612&w=0&k=20&c=xO1K6beBtVaheYpgElZcWxHD0otQDD23nV9FTCQkISo="
            alt="No movies available"
          />
        </div>
      );
    }
  }

  return (
    <div className="movie-list d-flex justify-content-evenly container">

      {
        handleMovies(movies)
      }

    </div>
  )
}
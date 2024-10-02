import MovieCard from "./MovieCard"

export const MovieList = ({ movies = [], loading }) => {

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
  
    if (movies.length > 0) {
      return (
        <div className="movie-list container">
          {movies.map((movie) => (
            <MovieCard key={movie.id} movie={movie} />
          ))}
        </div>
      );
    } else {
      return (
        <div style={{ display: 'flex' }}>
          <h3><i>Search not found</i></h3>
          <img
            style={{ maxWidth: '50%', maxHeight: '50%' }}
            src="https://media.istockphoto.com/id/1269500670/vector/yellow-rubber-duck-icon.jpg?s=612x612&w=0&k=20&c=xO1K6beBtVaheYpgElZcWxHD0otQDD23nV9FTCQkISo="
            alt="No movies available"
          />
        </div>
      );
    }
  }
  
import { useCallback, useRef, useEffect } from "react";
import MovieCard from "./MovieCard"
import { LoadingPage } from '../utils/LoadingPage';

export const MovieList = ({ movies = [], loading, onWishlist, currentPage, onPageChange, totalPages }) => {

  const observer = useRef();

  const lastMovieSet = useCallback(node => {
    if (loading) return

    console.log(totalPages, 'is the state of totalpages now in movielist.')
    if (observer.current) observer.current.disconnect()

    observer.current = new IntersectionObserver(entries => {
      if (entries[0].isIntersecting && !loading && currentPage <= totalPages) {
        onPageChange(currentPage + 1)
      }
    }, {
      threshold: 1.0 // Adjust threshold to load when the loadingRef is fully in view
  });
    if (node) observer.current.observe(node);

  }, [onPageChange]);

  return (
    <div className={`movie-list ${loading ? 'loading' : ''}`}>
      {movies.map((movie, index) => {
            const isLastMovie = index === movies.length - 1;
            return (
                <div key={movie.mv_id} ref={isLastMovie ? lastMovieSet : null}>
                    <MovieCard movie={movie} onWishlist={onWishlist} />
                </div>
            );
        })}

      {/* Render the loading spinner at the bottom of the movie list when fetching new movies */}
      {loading ? (
        <div className="loading-spinner">
          <LoadingPage />
        </div>
      ) : null}
    </div>
  );
};
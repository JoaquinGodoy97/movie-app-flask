import { useCallback, useRef, useEffect, useState } from "react";
import MovieCard from "./MovieCard"
import { LoadingPage } from '../utils/LoadingPage';

export const MovieList = ({ movies = [], loading, onWishlist, currentPage, onPageChange, totalPages, infiniteScroll }) => {

  const observer = useRef();

  const lastMovieSet = useCallback(node => {
    if (loading || !infiniteScroll) return

    if (observer.current) observer.current.disconnect()

    observer.current = new IntersectionObserver(entries => {
      if (entries[0].isIntersecting && !loading && currentPage < totalPages) {
        // console.log("Triggering onPageChange with new page:", currentPage + 1);
        onPageChange(currentPage + 1)
      }
    }, {
      threshold: 1.0 // Adjust threshold to load when the loadingRef is fully in view
    });
    if (node) observer.current.observe(node);

  }, [onPageChange, currentPage]);

  const loadingOverListStyle = {
    position: !infiniteScroll ? 'absolute' : null,
    top: !infiniteScroll ? '10%' : null,
  }

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

      {loading ? (
        <div className="loading-spinner " style={loadingOverListStyle}>
          <LoadingPage />
        </div>
      ) : (
        <>
          {movies.length <= 1 && !movies ? <div>No Movies Found.</div> : null}
        </>
      )}
      
    </div>
  );
};
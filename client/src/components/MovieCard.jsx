const MovieCard = ({ movie, onWishlist }) => {

    const POSTER_URL = "https://image.tmdb.org/t/p/w200"

    const checkPoster = (poster) => poster === null
        ? 'https://eticketsolutions.com/demo/themes/e-ticket/img/movie.jpg'
        :  POSTER_URL + poster

    return (

        <div className="card mb-3 me-5 movie-item" style={{ width: '12rem'}}>
            <div className=" position-absolute top-0 end-0 translate-middle">

                <button type="button" className="btn-sm" onClick={() => onWishlist(movie.id, movie.title)}
                    style={{ color: '#347a2e'}}>
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            width="26"
                            height="26"
                            fill="currentColor"
                            className="bi bi-bookmark-heart-fill"
                            viewBox="0 0 16 16"
                        >
                            <path d="M2 15.5a.5.5 0 0 0 .74.439L8 13.069l5.26 2.87A.5.5 0 0 0 14 15.5V2a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2zM8 4.41c1.387-1.425 4.854 1.07 0 4.277C3.146 5.48 6.613 2.986 8 4.412z" />
                        </svg>
                </button>
            </div>
            <img
                src={checkPoster(movie.poster_path)}
                className="card-img-top"
                alt="movie_cover"
            />
            <div className="card-body">
            <h5 className="card-title">{movie.title}</h5>
            <button
            type="button"
            className="btn btn-secondary mt-3"
            title={movie.overview}
            >More info</button>

            </div>
        </div>

    );
};

export default MovieCard;
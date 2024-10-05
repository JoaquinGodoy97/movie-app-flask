import { ToggleOverview } from "./utils/ToggleOverview";

const MovieCard = ({ movie, onWishlist }) => {

    const POSTER_URL = "https://image.tmdb.org/t/p/w200"
    const isOnWishlistPage = window.location.pathname.includes("/wishlist");

    const checkPoster = (poster) => poster === null
        ? 'https://eticketsolutions.com/demo/themes/e-ticket/img/movie.jpg'
        : POSTER_URL + poster

    if (!movie.overview) {
        movie.overview = movie.title
    }

    return (

        <div className="card movie-item">
            <div className="card-content">

                <a type="button" className="btn-sm" onClick={() => {
                    if (isOnWishlistPage) {
                        // console.log("deleted")
                        onWishlist(movie.mv_id);
                    } else {
                        // console.log("added")
                        onWishlist(movie.mv_id, movie.title);
                    }
                }}
                >
                    {/* TOGGLE BETWEEN /RESULTS ADDING BUTTONS AND /WISHLIST DELETE BUTTONS */}
                    {isOnWishlistPage ? (
                        <svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" fill="Currentcolor" className="bi bi-bookmark-x-fill" viewBox="0 0 16 16" style={{ color: '#cc3333' }}>
                            <path fillRule="evenodd" d="M2 15.5V2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v13.5a.5.5 0 0 1-.74.439L8 13.069l-5.26 2.87A.5.5 0 0 1 2 15.5M6.854 5.146a.5.5 0 1 0-.708.708L7.293 7 6.146 8.146a.5.5 0 1 0 .708.708L8 7.707l1.146 1.147a.5.5 0 1 0 .708-.708L8.707 7l1.147-1.146a.5.5 0 0 0-.708-.708L8 6.293z" />
                        </svg>
                    ) : (
                        <svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" fill="currentColor" className="bi bi-bookmark-heart-fill" viewBox="0 0 16 16" style={{ color: '#49c73d' }}>
                            <path d="M2 15.5a.5.5 0 0 0 .74.439L8 13.069l5.26 2.87A.5.5 0 0 0 14 15.5V2a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2zM8 4.41c1.387-1.425 4.854 1.07 0 4.277C3.146 5.48 6.613 2.986 8 4.412z" />
                        </svg>
                    )}

                </a>
            </div>
            
            <div className="card-element card-img" >
                <img
                    src={checkPoster(movie.poster_path)}
                    className="card-img-top"
                    alt="movie_cover"
                />
            </div>

                <div  className="card-element card-body">
                    <h5 className="card-title">{movie.title}</h5>

                    <ToggleOverview className="card-overview" overview={movie.overview} />
                </div>
        </div>

    );
};

export default MovieCard;
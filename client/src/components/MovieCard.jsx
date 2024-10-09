import { useState, useEffect } from "react";
import { Button } from "react-bootstrap";
import { ToggleOverview } from "./utils/ToggleOverview";

const MovieCard = ({ movie, onWishlist }) => {

    const [itemInWishlist, setItemInWishlist] = useState(false);
    const [data, setData] = useState('')

    useEffect(() => {

        const token = localStorage.getItem('token');
        fetch(`/wishlist-status/${movie.mv_id}`, {
            
            headers: {
                'Authorization': `Bearer ${token}`  // Send the token in Authorization header
            },
            credentials: 'include'
            
        })
            .then(response => response.json())
            .then(data => setItemInWishlist(data.in_wishlist))
            .catch(error => console.error('Error:', error));

    }, [movie.mv_id]);

    const handleWishlistToggle = () => {
        if (itemInWishlist) {
            onWishlist(movie.mv_id, movie.title, itemInWishlist);  // Call the removal action
            setItemInWishlist(false);  // Update state to remove from wishlist
        } else {
            onWishlist(movie.mv_id, movie.title, itemInWishlist);  // Call the add action
            setItemInWishlist(true);  // Update state to add to wishlist
        }
    };

    const [isHovered, setIsHovered] = useState(false);

    // Handler functions for mouse events
    const handleMouseEnter = () => setIsHovered(true);
    const handleMouseLeave = () => setIsHovered(false);

    // Dynamic styles box-shadow: inset 0 0 10px;
    const cardStyle = {
        transition: 'opacity 0.3s ease, box-shadow 0.3s ease', // 
        opacity: isHovered ? 0.9 : 1, // Change opacity when hovered/
        boxShadow: isHovered ? 'inset rgb(0, 0, 0) 0px 0px 60px -12px' : null,// Darken the card when hovered
        // backgroundColor: isHovered ? 'rgba(0, 0, 0, 0.235)' : '#f8f9fa', // Darken the card when hovered
    };

    const POSTER_URL = "https://image.tmdb.org/t/p/w200"
    const isOnWishlistPage = window.location.pathname.includes("/wishlist");

    const checkPoster = (poster) => poster === null
        ? 'https://eticketsolutions.com/demo/themes/e-ticket/img/movie.jpg'
        : POSTER_URL + poster


    if (!movie.overview) {
        movie.overview = movie.title
    }

    return (

        <div className="card movie-card" style={cardStyle}>
            <div className="card-content">

                <Button type="button" className="btn-sm" onClick={() => {
                    if (isOnWishlistPage) {
                        // console.log("deleted")
                        onWishlist(movie.mv_id);
                    } else {
                        // console.log("added")
                        handleWishlistToggle()
                    }
                }}
                onMouseEnter={handleMouseEnter}
                onMouseLeave={handleMouseLeave}
                >
                    {/* TOGGLE BETWEEN /RESULTS ADDING BUTTONS AND /WISHLIST DELETE BUTTONS */}
                    {isOnWishlistPage ? (
                        // REMOVE FROM WISHLIST (/WISHLIST)
                        <svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" fill="Currentcolor" className="bi bi-bookmark-x-fill add-wishlist-btn" viewBox="0 0 16 16" style={{ color: '#cc3333' }}>
                            <path fillRule="evenodd" d="M2 15.5V2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v13.5a.5.5 0 0 1-.74.439L8 13.069l-5.26 2.87A.5.5 0 0 1 2 15.5M6.854 5.146a.5.5 0 1 0-.708.708L7.293 7 6.146 8.146a.5.5 0 1 0 .708.708L8 7.707l1.146 1.147a.5.5 0 1 0 .708-.708L8.707 7l1.147-1.146a.5.5 0 0 0-.708-.708L8 6.293z" />
                        </svg>
                    ) : (
                        // ADD FROM RESULTS (/RESULTS/SEARCH)
                        <svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" fill="currentColor" className="bi bi-bookmark-heart-fill remove-wishlist-btn" viewBox="0 0 16 16" 
                        style={{ color: itemInWishlist ? '#CC3333' : '#f8f9fa' }}>
                            <path d="M2 15.5a.5.5 0 0 0 .74.439L8 13.069l5.26 2.87A.5.5 0 0 0 14 15.5V2a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2zM8 4.41c1.387-1.425 4.854 1.07 0 4.277C3.146 5.48 6.613 2.986 8 4.412z" />
                        </svg>
                    )}

                </Button>
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
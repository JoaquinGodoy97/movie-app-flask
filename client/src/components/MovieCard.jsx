import { useState } from "react";
import { Button } from "react-bootstrap";
import { ToggleOverview } from "../utils/ToggleOverview";
import React, { memo } from 'react';

const MovieCard = memo (({ movie, onWishlist }) => {

    // const [data, setData] = useState('')
    const [processingAction, setprocessingAction] = useState(false);
    const [isHidden, setIsHidden] = useState(false)

    const handleWishlistToggle = async () => {

        setprocessingAction(true)
        try {
            if (movie.inWishlist || atWishlistPage) {
                await onWishlist(movie.mv_id, movie.title, true); 
                // Call the removal action
                if (atWishlistPage) {
                    setIsHidden(true); // Hide the card if it's removed on the Wishlist Page
                }
            } else {
                await onWishlist(movie.mv_id, movie.title, false);  // Call the add action
            }
        } catch (err) {
            console.log(err)
        } 
        finally {
            setprocessingAction(false)
        }
    };

    const [isHovered, setIsHovered] = useState(false);

    // Handler functions for mouse events
    const handleMouseEnter = () => setIsHovered(true);
    const handleMouseLeave = () => setIsHovered(false);

    // Dynamic styles box-shadow: inset 0 0 10px;
    const cardStyle = {
        opacity: isHovered ? 0.9 : 1, // Change opacity when hovered/
        boxShadow: isHovered ? 'inset rgb(0, 0, 0) 0px 0px 60px -12px' : null,// Darken the card when hovered
        transform: isHidden ? 'scale(0%)' : null, // Apply CSS to hide the card
        overflow: isHidden ? 'hidden' : null, // Apply CSS to hide the card
        opacity: isHidden ? 0.5 : 1,
        animation: isHidden ? 'shrinkOut 0.6s ease-out forwards' : null,
        
    };

    const POSTER_URL = "https://image.tmdb.org/t/p/w200"
    const atWishlistPage = window.location.pathname.includes("/wishlist");

    const checkPoster = (poster) => poster === null
        ? 'https://eticketsolutions.com/demo/themes/e-ticket/img/movie.jpg'
        : POSTER_URL + poster


    if (!movie.overview) {
        movie.overview = movie.title
    }

    return (

        <div className={`card movie-card ${isHidden ? 'hidden' : ''}`} style={cardStyle}>
            <div className="card-content">

                <Button type="button" disabled={processingAction} className="btn-sm"
                onMouseEnter={handleMouseEnter}
                onMouseLeave={handleMouseLeave}
                onClick={handleWishlistToggle}
                >
                    {/* TOGGLE BETWEEN /RESULTS ADDING BUTTONS AND /WISHLIST DELETE BUTTONS */}
                        {/* // ADD FROM RESULTS (/RESULTS/SEARCH)
                        // <svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" fill="currentColor" className="bi bi-bookmark-heart-fill remove-wishlist-btn" viewBox="0 0 16 16" 
                        // style={{ color: movie.inWishlist ? '#CC3333' : '#f8f9fa' }}>
                        //     <path d="M2 15.5a.5.5 0 0 0 .74.439L8 13.069l5.26 2.87A.5.5 0 0 0 14 15.5V2a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2zM8 4.41c1.387-1.425 4.854 1.07 0 4.277C3.146 5.48 6.613 2.986 8 4.412z" />
                        // </svg> */}
                        <label class="wishlist-btn-container">
                        <input 
                        onChange={handleWishlistToggle}
                        checked={ atWishlistPage ? !movie.inWishlist : movie.inWishlist} type="checkbox" />

                        <div class="checkmark">
                            <svg viewBox="0 0 256 256">
                            <rect fill="none" height="256" width="256"></rect>
                            <path
                                d="M224.6,51.9a59.5,59.5,0,0,0-43-19.9,60.5,60.5,0,0,0-44,17.6L128,59.1l-7.5-7.4C97.2,28.3,59.2,26.3,35.9,47.4a59.9,59.9,0,0,0-2.3,87l83.1,83.1a15.9,15.9,0,0,0,22.6,0l81-81C243.7,113.2,245.6,75.2,224.6,51.9Z"
                                stroke-width="20px"
                                stroke="#000"
                                fill="none"
                            ></path>
                            </svg>
                        </div>
                        </label>

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
});

export default MovieCard;
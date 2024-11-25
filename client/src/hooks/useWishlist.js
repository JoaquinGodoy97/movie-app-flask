import { useCallback } from 'react';

export const useWishlist = (showToast, setMovies) => {

    const atWishlistPage = window.location.pathname.includes("/wishlist");

    const fetchWishlistStatuses = useCallback(async (movies) => {
        if (movies.length === 0) return; 
    
        try {
            const token = localStorage.getItem('token');
            const movieIds = movies.map(movie => movie.mv_id);
            const response = await fetch('/wishlist-status', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                credentials: 'include',
                body: JSON.stringify({ movie_ids: movieIds })
            });
    
            // Update with wishlist status
            const data = await response.json();

            console.log("Movie data status: ", data)

            setMovies(movies.map(movie => ({
                ...movie,
                inWishlist: data.statuses[movie.mv_id] || false // Default to false if not found
            })));

        } catch (err) {
            console.log("Unable to fetch:", err)
        } 

    }, [setMovies]);

    const handleWishlist = useCallback(async (id, name = "", currentInWishlist) => {
        
        try {
            // If a movie name has "/" slash turn it to "-"
            const fixMovieName = (name) => {
                if (name.includes("/")) {
                    return name.replace(/\//g, "-");
                }
                return name; // Return the original name if no "/" is found
            };

            const token = localStorage.getItem('token')
            const movie_name = fixMovieName(name);

            const url = currentInWishlist ?
                `http://localhost:5000/wishlist/remove/${id}`:
                `http://localhost:5000/wishlist/add/${id}/${movie_name}`;

            const options = {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                credentials: 'include',
                mode: 'cors',
            };

            const response = await fetch(url, options);
            const data = await response.json();

            if (response.ok && data.message) {

                // Update the movie's `inWishlist` status in the `movies` array
                if (data.method === 'remove' && atWishlistPage) {
                    setTimeout(() => {
                        setMovies((prevMovies) => prevMovies.filter((movie) => movie.mv_id !== id)); // Remove after transition
                    }, 1000); // Match the transition duration (0.6s)

                } else {
                    setMovies((prevMovies) => prevMovies.map((movie) =>
                        movie.mv_id === id ? { ...movie, inWishlist: !currentInWishlist } : movie
                    ));
                }
                showToast(data.message)
            }
        } catch (error) {
            console.error("Unable to add:", error)
        }
    }, [showToast, setMovies, atWishlistPage]);

    return { fetchWishlistStatuses, handleWishlist };

}
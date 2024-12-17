import { useState, useCallback, useRef } from 'react';

export const useFetchMovies = () => {
    const abortController = useRef(new AbortController()); // Create a new controller
    const [movies, setMovies] = useState([]);
    const [totalPages, setTotalPages] = useState(1);

    const fetchMovies = useCallback(async (query, page = 1, infiniteScroll) => {
        // Abort the previous request if still active
        if (abortController.current) {
            abortController.current.abort();
        }
        // Create a new controller for the new request
        abortController.current = new AbortController();
        const atWishlistPage = window.location.pathname.includes("/wishlist");
        
        try {
            let url;
            const apiBaseUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000';
            const token = localStorage.getItem('token');
            const options = {
                method: 'GET',
                headers: {
                    Authorization: `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                signal: abortController.current.signal,
            };
            if (atWishlistPage) {

                url = query
                    ? `${apiBaseUrl}/wishlist/search?query=${query}&page=${page}`
                    : `${apiBaseUrl}/wishlist?page=${page}`;
                    
            } else {
                url = `${apiBaseUrl}/results/search?query=${query}&page=${page}`;
            }

            const response = await fetch(url, options);
            const data = await response.json();

            if (data.results && data.total_pages) {
                setTotalPages(data.total_pages || 1);

                if (!infiniteScroll){
                    setMovies(data.results)
                } else {
                    setMovies((prevMovies) => [...prevMovies, ...data.results]);
                }

            } 
            
            // else {
            //     console.log("No more results. Last page.");
            // }
        } catch (error) {
            if (error.name === 'AbortError') {
                // console.log('Fetch aborted: A new request was started or component unmounted.');
            } else {
                console.error('Error fetching movies:', error);
            }
        }
    }, []);

    return { movies, setMovies, totalPages, fetchMovies };
};

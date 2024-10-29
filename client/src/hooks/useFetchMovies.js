import { useState, useCallback } from 'react';

export const useFetchMovies = () => {
    const [movies, setMovies] = useState([]);
    const [totalPages, setTotalPages] = useState(1);

    const fetchMovies = useCallback(async (query, page = 1, infiniteScroll) => {
        const atWishlistPage = window.location.pathname.includes("/wishlist");
        try {
            let url;
            const token = localStorage.getItem('token');
            const options = {
                method: 'GET',
                headers: {
                    Authorization: `Bearer ${token}`,
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
            };
            if (atWishlistPage) {
                url = query
                    ? `http://localhost:5000/wishlist/search?query=${query}&page=${page}`
                    : `http://localhost:5000/wishlist?page=${page}`;
            } else {
                url = `http://localhost:5000/results/search?query=${query}&page=${page}`;
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

            } else {
                console.log("No more results. Last page.");
            }
        } catch (error) {
            console.error('Error fetching movies:', error);
        }
    }, []);

    return { movies, setMovies, totalPages, fetchMovies };
};

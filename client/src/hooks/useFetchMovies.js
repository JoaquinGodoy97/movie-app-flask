

import { useState, useEffect } from 'react'

export const useFetchMovies = () => {

    const [movies, setMovies] = useState([]);
    const [totalPages, setTotalPages] = useState(1);
    const [newMovies, setNewMovies] = useState([]);

    const fetchMovies = async (query, page = 1, setLoading) => {
        setLoading(true)

        try {
            const token = localStorage.getItem('token')
            const response = await fetch(`http://localhost:5000/results/search?query=${query}&page=${page}`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                credentials: 'include',
            });

            const data = await response.json();
            console.log("Fetched movies:", data);
            // setNewMovies(data.results);
            console.log(newMovies)
            setMovies(prevMovies => [...prevMovies, ...data.results])
            setTotalPages(data.total_pages || 1);

        } catch (error) {
            console.error('Error fetching movies:', error);
        } finally {
            setLoading(false);
        }

    };

    useEffect(() => {
        if (newMovies.length > 0) {
            setMovies((prevMovies) => [...prevMovies, ...newMovies]);
        }
    }, [newMovies]);

    return { movies, setMovies, totalPages, fetchMovies };


}


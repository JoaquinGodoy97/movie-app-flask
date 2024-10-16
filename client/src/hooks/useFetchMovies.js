import { useState } from 'react'

export const useFetchMovies = () => {

    const [movies, setMovies] = useState([]);
    const [totalPages, setTotalPages] = useState(1);

    const fetchMovies = async (query, page = 1, setLoading) => {

        const atWishlistPage = window.location.pathname.includes("/wishlist");

        setLoading(true)
        try {

            let url;
            const token = localStorage.getItem('token')
            const options = {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                credentials: 'include',
            }

            if (atWishlistPage){
                url = query ?
                    `http://localhost:5000/wishlist/search?query=${query}&page=${page}` :
                    `http://localhost:5000/wishlist?page=${page}`;
            } else {
                url = `http://localhost:5000/results/search?query=${query}&page=${page}`;
            }
            
            const response = await fetch(url, options);

            const data = await response.json();
            console.log("Fetched movies:", data);
            // if (atWishlistPage){
            //     setMovies(prevMovies => [...prevMovies, ...data.results])
            // } else {
            setMovies(prevMovies => [...prevMovies, ...data.results])
            // }
            // setMovies(data.results)
            
            setTotalPages(data.total_pages || 1);

        } catch (error) {
            console.error('Error fetching movies:', error);
        } finally {
            setLoading(false);
        }

    };

    // useEffect(() => {
    //     if (movies.length > 0) {
    //         setMovies((prevMovies) => [...prevMovies, ...movies]);
    //     }
    // }, [movies]);

    return { movies, setMovies, totalPages, fetchMovies };

}


import React, { useState, useEffect } from 'react'
import { SearchBar } from './SearchBar'
import { MovieList } from './MovieList';
import { PaginationPanel } from './PaginationPanel';
import { useLocation, useNavigate } from 'react-router-dom';
import '../Main.css';

const WishlistPage = () => {

    const [movies, setMovies] = useState([]);
    const [totalPages, setTotalPages] = useState(1);
    const navigate = useNavigate();

    const location = useLocation();
    const queryParams = new URLSearchParams(location.search)
    const searchQuery = queryParams.get('query') || "";
    const currentPageUrl = parseInt(queryParams.get('page')) || 1;
    const [loading, setLoading] = useState(false);
    const [user, setUser] = useState("");


    const fetchMovies = async (query, page = 1) => {
        setLoading(true)

        try {

            const userData = await fetch("http://localhost:5000/@me", {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include',
            mode: 'cors',
            })

            console.log(userData)

            const url = query ?
                `http://localhost:3000/wishlist/search?query=${query}&page=${page}` :
                `http://localhost:3000/wishlist?page=${page}`;

            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: 'include',
                mode: 'cors',
            });

            const result = await response.json();

            if (response.ok) {
                setMovies(result.results);
                setTotalPages(result.total_pages || 1);
            } else {
                alert(result.error);
            }
        } catch (error) {
            console.error('Error fetching movies: ', error);
        } finally {
            setLoading(false)
        }

    };

    useEffect(() => {
        fetchMovies(searchQuery, currentPageUrl);
    }, [searchQuery, currentPageUrl]);

    const handleSearch = (query) => {
        if (!query) {
            navigate(`/wishlist?page=1`);
        }

        // Navigate to the results page with the search query
        // navigate(`/wishlist/search?query=${query}&page=1`);
    };


    const handlePageChange = (newPage) => {
        if (newPage > 0 && newPage <= totalPages) {
            // Fetch new data based on the current query and page
            console.log(`Fetching data for page: ${newPage}`);

            // If there is no search query, go to /wishlist
            if (!searchQuery) {
                navigate(`/wishlist/?page=${newPage}`);
            } else {
                // If there is a search query, go to /wishlist/search
                navigate(`/wishlist/search?query=${searchQuery}&page=${newPage}`);
            }
        }
    };

    return (
        <div className="results-page">


            <SearchBar
                onSearch={handleSearch}
                currentPage={currentPageUrl}
                totalPages={totalPages}
            />

            {totalPages > 0 ?

                <PaginationPanel currentPage={currentPageUrl} totalPages={totalPages} onPageChange={handlePageChange} />

                : null}

            <MovieList movies={movies} loading={loading} />
        </div>
    )
}

export default WishlistPage
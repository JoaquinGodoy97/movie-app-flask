import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom'; // Import useLocation to access the query
import { useNavigate } from 'react-router-dom';
import SearchBar from './SearchBar';
import MovieList from './MovieList';
import PaginationPanel from './PaginationPanel';
import '../Main.css';

const ResultsPage = () => {
    const [movies, setMovies] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const navigate = useNavigate();

    // Use location to read the query from the URL
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const searchQuery = queryParams.get('query') || '';

    const fetchMovies = async (query, page = 1) => {
        try {
            const response = await fetch(`http://localhost:5000/results/search?query=${query}&page=${page}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: 'include',
            });

            const data = await response.json();
            setMovies(data.results);
            console.log(data.total_pages)
            setTotalPages(data.total_pages || 1);

        } catch (error) {
            console.error('Error fetching movies:', error);
        }
    };

    // This effect runs whenever the searchQuery or currentPage changes
    useEffect(() => {
        if (searchQuery) {
            fetchMovies(searchQuery, currentPage); // Trigger the fetch with the search query
        }
    }, [searchQuery, currentPage]);

    const handleSearch = (query) => {
        if (!query) {
            alert("Please enter a search term");
            return;
        }

        setCurrentPage(1)
        // Navigate to the results page with the search query
        navigate(`/results/search?query=${query}&page=1`);
    };

    const handlePageChange = (newPage) => {
        if (newPage > 0 && newPage <= totalPages) {
            setCurrentPage(newPage);
            // Add logic here to fetch new data based on the page (if needed)
            console.log(`Fetching data for page: ${newPage}`);
            navigate(`/results/search?query=${searchQuery}&page=${newPage}`);
        }
    };

    // const handleWishlist = (movieId, movieTitle) => {

    //     console.log(`Added movie ${movieTitle} to wishlist,`)
    // }

    return (
        <div className="results-page">
            <SearchBar
                onSearch={handleSearch}
                currentPage={currentPage}
                totalPages={totalPages}
            />
            <PaginationPanel currentPage={currentPage} totalPages={totalPages} onPageChange={handlePageChange} />

            <MovieList movies={movies} />
        </div>
    );

};

export default ResultsPage;
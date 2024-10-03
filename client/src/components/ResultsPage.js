import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom'; // Import useLocation to access the query
import { SearchBar } from './SearchBar';
import { MovieList } from './MovieList';
import { PaginationPanel } from './PaginationPanel';
import '../Main.css';
import { checkUserSession } from './checkUserSession';
import { LoadingPage } from './utils/LoadingPage';

const ResultsPage = () => {
    const [movies, setMovies] = useState([]);
    const [totalPages, setTotalPages] = useState(1);
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);

    // Use location to read the query from the URL
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const searchQuery = queryParams.get('query') || '';
    const [user, setUser] = useState(null);
    const currentPageUrl = parseInt(queryParams.get('page')) || 1;

    const fetchMovies = async (query, page = 1) => {
        setLoading(true)

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
            console.log(data.results)
            setTotalPages(data.total_pages || 1);
            console.log("total pages:", data.total_pages)

        } catch (error) {
            console.error('Error fetching movies:', error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        const checkSessionAndFetchMovies = async () => {
            await checkUserSession(setLoading, setUser, navigate);
            if (searchQuery && currentPageUrl) {
                await fetchMovies(searchQuery, currentPageUrl);
            }
        };
        checkSessionAndFetchMovies();
    }, [searchQuery, currentPageUrl, navigate]);

    // This effect runs whenever the searchQuery or currentPage changes
    // useEffect(() => {
    //     if (searchQuery && currentPageUrl) {
    //         fetchMovies(searchQuery, currentPageUrl); 
    //     }

    // }, [searchQuery, currentPageUrl]);

    const handleSearch = (query) => {
        if (!query) {
            alert("Please enter a search term");
            return;
        }

        // Navigate to the results page with the search query
        navigate(`/results/search?query=${query}&page=1`);
    };

    const handlePageChange = (newPage) => {
        if (newPage > 0 && newPage <= totalPages) {
            // Add logic here to fetch new data based on the page (if needed)
            console.log(`Fetching data for page: ${newPage}`);
            navigate(`/results/search?query=${searchQuery}&page=${newPage}`);
        }
    };

    const handleWishlist = async (id, name = "") => {
        try {
            const url = `http://localhost:5000/wishlist/add/${id}/${name}`;

            const options = {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: 'include',
                mode: 'cors',
            };

            const response = await fetch(url, options);
            const result = await response.json();

            console.log(result)

            if(result.error){
                return alert(result.error)
            } else{
                return alert(result.message)
            }

        } catch (error) {
            console.error("Unable to remove:", error)
        }
    };

    const classNames = `results-page main-item movie-search d-flex mt-5 mb-3 montserrat-font ${!loading ? 'fade-in' : ''}`

    if (loading) {
        return <LoadingPage />
    }

    return (
        <div className={classNames}>
            <SearchBar
                onSearch={handleSearch}
            />
            {(totalPages && currentPageUrl <= totalPages) ?

                <PaginationPanel currentPage={currentPageUrl} totalPages={totalPages} onPageChange={handlePageChange} />

                : null}


            <MovieList movies={movies} loading={loading} onWishlist={handleWishlist} />

        </div>
    );

};

export default ResultsPage;
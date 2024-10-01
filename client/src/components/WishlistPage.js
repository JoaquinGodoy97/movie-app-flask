import React, { useState, useEffect } from 'react'
import { SearchBar } from './SearchBar'
import {MovieList} from './MovieList';
import {PaginationPanel} from './PaginationPanel';
import { useLocation, useNavigate } from 'react-router-dom';
import '../Main.css';

const WishlistPage = () => {

    const [ movies, setMovies ] = useState([]);
    const [totalPages, setTotalPages ] = useState(1);
    const navigate = useNavigate();
    const sessionData = useState(localStorage.getItem('session'))

    const location = useLocation();
    const queryParams = new URLSearchParams(location.search)
    const searchQuery = queryParams.get('query') || "";
    const currentPageUrl = queryParams.get('page') || 1;
    const [loading, setLoading] = useState(false);

    const fetchMovies = async ( query, page = 1) => {
        setLoading(true)

        try{
            const response = await fetch(`http://localhost:5000/wishlist/search?query=${query}&page=${page}`,{
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: 'include',
            });

            const data = await response.json() 
            
            console.log(data)

            setMovies(data.results);
            console.log(data.results)
            setTotalPages(data.total_pages || 1);
            console.log(totalPages)

        } catch (error){
            console.error('Error fetching movies: ', error);
        } finally {
            setLoading(false)
        }

    };

    useEffect(() => {
        if (searchQuery && currentPageUrl) {
            fetchMovies(searchQuery, currentPageUrl); 
        }

    }, [searchQuery, currentPageUrl]);

    const handleSearch = (query) => {
        if (!query) {
            navigate(`/wishlist/search?query=&page=1`);
        }

        // Navigate to the results page with the search query
        navigate(`/wishlist/search?query=${query}&page=1`);
    };
    

    const handlePageChange = (newPage) => {
        if (newPage > 0 && newPage <= totalPages) {
            // Add logic here to fetch new data based on the page (if needed)
            console.log(`Fetching data for page: ${newPage}`);
            navigate(`/results/search?query=${searchQuery}&page=${newPage}`);
        }
    };


    return (
        <div className="results-page">

            { totalPages === 0 ? 
            
            <PaginationPanel currentPage={currentPageUrl} totalPages={totalPages} onPageChange={handlePageChange} />
            
            : null}
            <SearchBar
                onSearch={handleSearch}
                currentPage={currentPageUrl}
                totalPages={totalPages}
            />
            

            <MovieList movies={movies} loading={loading} />
        </div>
    )
}

export default WishlistPage
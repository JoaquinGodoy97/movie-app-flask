import React, { useState, useEffect } from 'react'
import { SearchBar } from './SearchBar'
import { MovieList } from './MovieList';
import { PaginationPanel } from './PaginationPanel';
import { useLocation, useNavigate } from 'react-router-dom';
import '../Main.css';
import { checkUserSession } from './checkUserSession';
import { LoadingPage } from './utils/LoadingPage';

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


    useEffect(() => {

        const fetchMovies = async (query, page = 1) => {
            setLoading(true)
            try {
                const url = query ?
                    `http://localhost:5000/wishlist/search?query=${query}&page=${page}` :
                    `http://localhost:5000/wishlist?page=${page}`;
    
                const response = await fetch(url, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    credentials: 'include',
                    mode: 'cors',
                });
    
                if (response.status === 401) {
                    navigate('/login');
                }
    
                const result = await response.json();
    
                if (response.ok) {
                    
                    setMovies(result.results);
                    console.log("What does movie have", result.results)
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

        const checkSessionAndFetchMovies = async () => {

            await checkUserSession(setLoading, setUser, navigate)

            if (searchQuery || currentPageUrl) {

                await fetchMovies(searchQuery, currentPageUrl);
            }
        };

        checkSessionAndFetchMovies();
    }, [searchQuery, currentPageUrl, navigate]);

    const handleSearch = (query) => {
        if (!query) {
            navigate(`/wishlist?page=1`);
        }
        navigate(`/wishlist/search?query=${query}&page=${currentPageUrl}`)

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
                navigate(`/wishlist/search?query=${searchQuery}&?page=${newPage}`);
            }
        }
    };

    const handleWishlist = async (id) => {
        try {
            const url = `http://localhost:5000/wishlist/remove/${id}`
        
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

            if (result.message){
                setMovies((oldMovieList) => oldMovieList.filter((movie)=> movie.mv_id !== id))
            } 
            // else if (result.message && !isOnWishlistPage) {
            //     setMovies((oldMovieList) => oldMovieList.filter((movie)=> movie.mv_id !== id))
            // }

        } catch (error) {
            console.error("Unable to remove:", error)
        }
    }

    const classNames = `results-page main-item movie-search d-flex mt-5 mb-3 ${!loading ? 'fade-in' : ''}`

    if (loading) {
        return <LoadingPage />
    }
    return (
        <div className={classNames}>
            <SearchBar
                onSearch={handleSearch}
            />
            {(totalPages && currentPageUrl <= totalPages && totalPages > 1) ?
                <PaginationPanel currentPage={currentPageUrl} totalPages={totalPages} onPageChange={handlePageChange} />
                : null}
            <MovieList movies={movies} loading={loading} onWishlist={handleWishlist} />
        </div>
    )
}

export default WishlistPage
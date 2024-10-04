import React, { useState, useEffect, useContext } from 'react'
import { SearchBar } from './SearchBar'
import { MovieList } from './MovieList';
import { PaginationPanel } from './utils/PaginationPanel';
import { useLocation, useNavigate } from 'react-router-dom';
import '../Main.css';
import { checkUserSession } from './checkUserSession';
import { LoadingPage } from './utils/LoadingPage';
import Switch from 'react-switch';
import { ThemeContext } from '../App'; // import the context

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

            if (result.message) {
                setMovies((oldMovieList) => oldMovieList.filter((movie) => movie.mv_id !== id))
            }
            // else if (result.message && !isOnWishlistPage) {
            //     setMovies((oldMovieList) => oldMovieList.filter((movie)=> movie.mv_id !== id))
            // }

        } catch (error) {
            console.error("Unable to remove:", error)
        }
    }

    const classNames = `main-item ${!loading ? 'fade-in' : ''}`
    const { theme, toggleTheme } = useContext(ThemeContext);

    return (
        <div className={classNames}>

            <nav className='nav-theme sub-container'>
                <Switch
                    onColor="#f5f490"
                    offColor="#333130"
                    checkedIcon={<span className="toggle-theme-mode" role="img" aria-label="sound-on">⛅</span>}
                    uncheckedIcon={<span className="toggle-theme-mode" role="img" aria-label="sound-off">🌘</span>}

                    className='switch' onChange={toggleTheme} checked={theme === 'dark'} />
            </nav>

            <div className='button-container sub-container'>

                    <SearchBar onSearch={handleSearch} />

                    <div class="side-buttons ms-3 mb-3">
                        <input onClick={() => { navigate('/logout') }} class="btn btn-outline-dark" name="logout" id="logout" type="submit" value="Log Out" />
                        <a onClick={() => { navigate('/search') }} class="btn btn-dark">
                            <svg xmlns="http://www.w3.org/2000/svg" width="30" height="23" fill="currentColor" class="bi bi-arrow-left-square" viewBox="0 0 16 16">
                                <path fill-rule="evenodd" d="M15 2a1 1 0 0 0-1-1H2a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1zM0 2a2 2 0 0 1 2-2h12a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H2a2 2 0 0 1-2-2zm11.5 5.5a.5.5 0 0 1 0 1H5.707l2.147 2.146a.5.5 0 0 1-.708.708l-3-3a.5.5 0 0 1 0-.708l3-3a.5.5 0 1 1 .708.708L5.707 7.5z" />
                            </svg>
                        </a>

                    </div>


            </div>
            <div className='content-container'>
                {loading ? (
                    // Show the loading component when loading is true
                    <LoadingPage />
                ) : (
                    <>
                        <MovieList movies={movies} loading={loading} onWishlist={handleWishlist} />

                        {totalPages && currentPageUrl <= totalPages && (
                            <PaginationPanel
                                className="pagination"
                                currentPage={currentPageUrl}
                                totalPages={totalPages}
                                onPageChange={handlePageChange}
                            />
                        )}
                    </>

                )}
            </div>
        </div>
    )
}

export default WishlistPage
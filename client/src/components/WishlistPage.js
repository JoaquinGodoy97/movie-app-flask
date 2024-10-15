import React, { useState, useEffect, useContext, useCallback} from 'react'
import { SearchBar } from '../utils/SearchBar'
import { MovieList } from './MovieList';
import { PaginationPanel } from '../utils/PaginationPanel';
import { useLocation, useNavigate } from 'react-router-dom';
import { checkUserSession } from './checkUserSession';
import { LoadingPage } from '../utils/LoadingPage';
import Switch from 'react-switch';
import { ThemeContext } from '../App';
import { useToast } from '../utils/ToastMessage';
import '../styles/Main.css';

const WishlistPage = () => {

    const [movies, setMovies] = useState([]);
    const [totalPages, setTotalPages] = useState(1);
    const navigate = useNavigate();
    const [wishlistFetched, setWishlistFetched] = useState(false);
    const location = useLocation();
    const queryParams = new URLSearchParams(location.search)
    const searchQuery = queryParams.get('query') || "";
    const currentPageUrl = parseInt(queryParams.get('page')) || 1;
    const [loading, setLoading] = useState(false);
    const [user, setUser] = useState("");
    const { showToast } = useToast();
    

    useEffect(() => {

        const fetchMovies = async (query, page = 1) => {
            setLoading(true)
            try {

                const token = localStorage.getItem('token');
                
                if (!token) {
                    // If there's no token, redirect to login or handle accordingly
                    console.log('No token found, redirecting to login.');
                    navigate("/login")
                    // Redirect logic here, e.g. navigate('/login');
                    return;
                }

                const url = query ?
                    `http://localhost:5000/wishlist/search?query=${query}&page=${page}` :
                    `http://localhost:5000/wishlist?page=${page}`;
                const options = {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json'
                    },
                    credentials: 'include',
                    mode: 'cors',
                }

                const response = await fetch(url, options);

                if (response.status === 401) {
                    navigate('/login');
                }

                const result = await response.json();

                if (response.ok) {

                    setMovies(result.results);
                    setTotalPages(result.total_pages || 1);
                    setWishlistFetched(false);
                } else {
                    showToast(result.error);
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

    useEffect(() => {
        const fetchWishlistStatuses = async (movies) => {
            const token = localStorage.getItem('token');
            const movieIds = movies.map(movie => movie.mv_id);

            const response = await fetch('/wishlist-status', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                credentials: 'include',
                body: JSON.stringify({ movie_ids: movieIds })
            });

            const data = await response.json();
            setMovies(movies.map(movie => ({
                ...movie,
                inWishlist: data.statuses[movie.mv_id]  // Update with wishlist status
            })));
        };

        if (!wishlistFetched && movies.length > 0) {
            fetchWishlistStatuses(movies);
            setWishlistFetched(true);  // Mark wishlist fetching as done
        }
    }, [movies, wishlistFetched]);  // Only run this effect after `movies` is fetched

    const handleSearch = (query) => {
        if (!query) {
            navigate(`/wishlist?page=1`);
        }
        navigate(`/wishlist/search?query=${query}&page=${currentPageUrl}`)

    };


    const handlePageChange = (newPage) => {
        if (newPage > 0 && newPage <= totalPages) {
            // console.log(`Fetching data for page: ${newPage}`);

            if (!searchQuery) {
                navigate(`/wishlist/?page=${newPage}`);
            } else {
                navigate(`/wishlist/search?query=${searchQuery}&?page=${newPage}`);
            }
        }
    };

    const handleWishlist = useCallback(async (id, title = "", itemInWishlist = true) => {

        // setLoading(true); 
        const token = localStorage.getItem('token')
        
        const url = `http://localhost:5000/wishlist/remove/${id}`
        const options = {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            credentials: 'include',
            mode: 'cors',
        };

        try {
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
        
    }, []);

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

                <div className="side-buttons ms-3 mb-3">
                    <input onClick={() => { navigate('/logout') }} className="btn btn-outline-dark" name="logout" id="logout" type="submit" value="Log Out" />
                    <a onClick={() => { navigate('/search') }} className="btn btn-dark">
                        <svg xmlns="http://www.w3.org/2000/svg" width="30" height="23" fill="currentColor" className="bi bi-house-door-fill" viewBox="0 0 16 16">
                            <path d="M6.5 14.5v-3.505c0-.245.25-.495.5-.495h2c.25 0 .5.25.5.5v3.5a.5.5 0 0 0 .5.5h4a.5.5 0 0 0 .5-.5v-7a.5.5 0 0 0-.146-.354L13 5.793V2.5a.5.5 0 0 0-.5-.5h-1a.5.5 0 0 0-.5.5v1.293L8.354 1.146a.5.5 0 0 0-.708 0l-6 6A.5.5 0 0 0 1.5 7.5v7a.5.5 0 0 0 .5.5h4a.5.5 0 0 0 .5-.5" />
                        </svg>
                    </a>

                </div>


            </div>
            <div className='content-container'>
                {loading ? (
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
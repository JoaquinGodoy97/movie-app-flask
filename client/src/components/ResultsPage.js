import { useCallback, useContext, useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom'; // Import useLocation to access the query
import Switch from 'react-switch';
import { ThemeContext } from '../App';
import { useFetchMovies } from '../hooks/useFetchMovies';
import { useWishlist } from '../hooks/useWishlist';
import '../styles/Main.css';
import { LoadingPage } from '../utils/LoadingPage';
import { PaginationPanel } from '../utils/PaginationPanel';
import { SearchBar } from '../utils/SearchBar';
import { useToast } from '../utils/ToastMessage';
import { checkUserSession } from './checkUserSession';
import { MovieList } from './MovieList';

const ResultsPage = () => {
    const [infiniteScroll, setInfiniteScroll] = useState(true);
    const { showToast } = useToast();
    // const [movies, setMovies] = useState([]);
    const [currentPage, setCurrentPage] = useState(1); // Track current page
    // const [totalPages, setTotalPages] = useState(1);
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);
    const [newMovies, setNewMovies] = useState([]); // Temporary state for new movies

    const location = useLocation();
    const queryParams = new URLSearchParams(location.search);
    const searchQuery = queryParams.get('query') || '';
    const [user, setUser] = useState(null);
    // const currentPageUrl = parseInt(queryParams.get('page')) || 1;
    const { movies, setMovies, totalPages, fetchMovies } = useFetchMovies();
    const { fetchWishlistStatuses, handleWishlist, tempMovies } = useWishlist(showToast, setMovies);
    const [wishlistFetched, setWishlistFetched] = useState(false)

    useEffect(() => {
        const pageFromUrl = parseInt(queryParams.get('page')) || 1;
        setCurrentPage(pageFromUrl);
    }, [location.search])

    useEffect(() => {
        const checkSessionAndFetchMovies = async () => {
            await checkUserSession(setLoading, setUser, navigate);

            // console.log("Search Query:", searchQuery);
            // console.log("Current Page:", currentPage);
            // console.log("Total Pages:", totalPages);

            if (searchQuery && currentPage <= totalPages) {
                if (currentPage === 1) {

                    setMovies([]); // Restarts movies everytime current page is 1.
                }
                await fetchMovies(searchQuery, currentPage, setLoading);
            }
        };
    
        checkSessionAndFetchMovies();
    }, [currentPage]);

    useEffect(() => {

        if (!wishlistFetched && movies.length > 0){
            fetchWishlistStatuses(movies);
            setWishlistFetched(true)
        }

    }, [movies, wishlistFetched, fetchWishlistStatuses]);

    // Resetting `wishlistFetched` only when `movies` change
    useEffect(() => {
        setWishlistFetched(false);
    }, [movies.length]);

    const handleSearch = useCallback((query) => {
        if (!query) {
            alert("Please enter a search term");
            return;
        }

        // Navigate to the results page with the search query
        navigate(`/results/search?query=${query}&page=1`);
    }, [navigate]);

    const handlePageChange = (newPage) => {
        if (newPage > 0 && newPage <= totalPages) {

            setCurrentPage(newPage)
            // navigate(`/results/search?query=${searchQuery}&page=${newPage}`);
        }
    };

    // useEffect(() => {
    //     if (newMovies.length > 0) {
    //         setMovies(prevMovies => [...prevMovies, ...newMovies]); // Append new movies
    //     }
    // }, [newMovies]); // Effect to merge new movies into the main list

    const classNames = `main-item montserrat-font ${!loading ? 'fade-in' : ''}`
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
                    <a onClick={() => { navigate('/wishlist') }} className="btn btn-dark">
                        <svg xmlns="http://www.w3.org/2000/svg" width="30" height="23" fill="currentColor" className="bi bi-book" viewBox="0 0 16 16" style={{ color: 'rgb(210, 210, 210)' }}>
                            <path d="M1 2.828c.885-.37 2.154-.769 3.388-.893 1.33-.134 2.458.063 3.112.752v9.746c-.935-.53-2.12-.603-3.213-.493-1.18.12-2.37.461-3.287.811zm7.5-.141c.654-.689 1.782-.886 3.112-.752 1.234.124 2.503.523 3.388.893v9.923c-.918-.35-2.107-.692-3.287-.81-1.094-.111-2.278-.039-3.213.492zM8 1.783C7.015.936 5.587.81 4.287.94c-1.514.153-3.042.672-3.994 1.105A.5.5 0 0 0 0 2.5v11a.5.5 0 0 0 .707.455c.882-.4 2.303-.881 3.68-1.02 1.409-.142 2.59.087 3.223.877a.5.5 0 0 0 .78 0c.633-.79 1.814-1.019 3.222-.877 1.378.139 2.8.62 3.681 1.02A.5.5 0 0 0 16 13.5v-11a.5.5 0 0 0-.293-.455c-.952-.433-2.48-.952-3.994-1.105C10.413.809 8.985.936 8 1.783" />
                        </svg>
                    </a>

                </div>
            </div>
            <div className='content-container'>
                {loading && !infiniteScroll ? (
                    // Show the loading component when loading is true
                    <LoadingPage />
                ) : (
                    // When loading is false, display PaginationPanel and MovieList
                    <>
                        {movies.length > 0 ? (
                            <>
                                <MovieList
                                    movies={movies}
                                    loading={loading}
                                    onWishlist={handleWishlist}
                                    onPageChange={handlePageChange}
                                    currentPage={currentPage}
                                />
                                {totalPages && currentPage <= totalPages && (
                                    <PaginationPanel
                                        currentPage={currentPage}
                                        totalPages={totalPages}
                                        onPageChange={handlePageChange}
                                    />
                                ) && !infiniteScroll}
                            </>
                        ) : (
                            !loading && <div>No movies found.</div> // Handle no movies case
                        )}
                    </>
                )}
            </div>

        </div>
    );
};

export default ResultsPage;
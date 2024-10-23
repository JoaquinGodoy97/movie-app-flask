import React, { useState, useEffect, useContext, useCallback, useMemo } from 'react'
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
import { useFetchMovies } from '../hooks/useFetchMovies';
import { useWishlist } from '../hooks/useWishlist';

const WishlistPage = () => {

    const navigate = useNavigate();
    const [wishlistFetched, setWishlistFetched] = useState(false);
    const location = useLocation();
    const queryParams = useMemo(() => new URLSearchParams(location.search), [location.search]);

    // const queryParams = new URLSearchParams(location.search)
    const searchQuery = queryParams.get('query') || "";
    const currentPageUrl = parseInt(queryParams.get('page')) || 1;
    const [loading, setLoading] = useState(false);
    const [user, setUser] = useState("");
    const { showToast } = useToast();
    const [currentPage, setCurrentPage] = useState(1);
    const { movies, setMovies, totalPages, fetchMovies } = useFetchMovies();
    const { fetchWishlistStatuses, handleWishlist } = useWishlist(showToast, setMovies);
    const [ infiniteScroll, setInfiniteScroll] = useState(true);
    const atWishlistPage = window.location.pathname.includes("/wishlist");


    useEffect(() => {
        // const pageFromUrl = parseInt(queryParams.get('page')) || 1;
        // if (pageFromUrl !== currentPage) {
        //     console.log(`Updating currentPage from URL: ${pageFromUrl}`);

        //     setCurrentPage(pageFromUrl);
        // }
    }, []);

    useEffect(() => {
        const checkSession = async () => {
            console.log('Checking user session...');
            const userSession = await checkUserSession(setLoading, setUser, navigate);
            if (!userSession) return;  // Stop if session is invalid
        };

        checkSession();  // Run session check only once on mount
    }, []);

    useEffect(() => {
        const fetchInitialMovies = async () => {
            console.log("Fetching movies for page:", currentPage);
            console.log("total pages:", totalPages)
            const resetMovies = currentPage === 1 && searchQuery.length > 0;

            if (totalPages >= 1 && atWishlistPage && !loading) {
                console.log(totalPages, "after")
                if (currentPage === 1) {
                    setMovies([]);  // Reset movies for the first page
                }
                await fetchMovies(searchQuery, currentPage, setLoading, resetMovies);
            }
        };

        fetchInitialMovies();
    }, [currentPage, searchQuery, fetchMovies]);

    // useEffect(() => {

    //     if (!wishlistFetched && movies.length > 0) {
    //         fetchWishlistStatuses(movies);
    //         setWishlistFetched(true);  // Mark wishlist fetching as done
    //     }


    // }, [movies, wishlistFetched, fetchWishlistStatuses]);  // Only run this effect after `movies` is fetched

    // useEffect(() => {
    //     setWishlistFetched(false);
    // }, [movies.length]);

    const handleSearch = useCallback((query, page) => {
        if (!query) {
            navigate(`/wishlist?page=1`);
        }

        setCurrentPage(1)
        navigate(`/wishlist/search?query=${query}&page=${page}`)
    }, []);



    const handlePageChange = (newPage) => {

        console.log(currentPage, newPage, newPage <= totalPages)
        console.log("Whats the state of movies length:", movies.length)

        if (newPage > currentPage && newPage <= totalPages){

            console.log("1st validation")
        }

        if (atWishlistPage && newPage > 0 && !loading) {
            console.log(`2d validation Changing page to: ${newPage}`);
            setCurrentPage(newPage)

            // navigate(`/wishlist?page=${newPage}`);
        }   else if (!atWishlistPage){

            console.log("3rd validation")
            navigate(`/wishlist/search?query=${searchQuery}&page=${newPage}`);
        }
        // if (newPage !== currentPage && newPage > 0 && newPage <= totalPages) {
    //         setCurrentPage(newPage);  // Update state directly
    //         if (!searchQuery) {
        
        // }
    } ;

    const classNames = `main-item ${!loading ? 'fade-in' : ''}`
    const { theme, toggleTheme } = useContext(ThemeContext);

    // if (loading){
    //     return <LoadingPage />
    // }

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
                {loading && !infiniteScroll? (
                    // Show the loading component when loading is true
                    <LoadingPage />
                ) : (
                    <>
                        {movies.length > 0 ? (
                            <>
                                <MovieList
                                    movies={movies}
                                    loading={loading}
                                    onWishlist={handleWishlist}
                                    onPageChange={handlePageChange}
                                    currentPage={currentPage}
                                    totalPages={totalPages}
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
    )
}

export default WishlistPage
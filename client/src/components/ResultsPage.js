import { useCallback, useContext, useEffect, useState, useMemo } from 'react';
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
import { MovieList } from './MovieList';
import { useCheckUserSession } from './checkUserSession';


const ResultsPage = () => {
    const navigate = useNavigate();
    const [wishlistFetched, setWishlistFetched] = useState(false)
    const location = useLocation();
    const [infiniteScroll, setInfiniteScroll] = useState(true);
    
    const queryParams = useMemo(() => new URLSearchParams(location.search), [location.search]);
    
    const { showToast } = useToast();
    const [currentPage, setCurrentPage] = useState(1); // Track current page
    const [loading, setLoading] = useState(false);
    const [loadingComponent, setLoadingComponent] = useState(false);

    const searchQuery = queryParams.get('query') || '';
    const { movies, setMovies, totalPages, fetchMovies } = useFetchMovies();
    const { fetchWishlistStatuses, handleWishlist } = useWishlist(showToast, setMovies);
    const atResultsPage = window.location.pathname.includes("/results");
    const { loading: sessionLoading, user: sessionUser } = useCheckUserSession();

    // useEffect(() => {
    //     const pageFromUrl = parseInt(queryParams.get('page')) || 1;
    //     setCurrentPage(pageFromUrl);
    // }, [location.search])
    // useEffect(() => {
    //     const checkSession = async () => {
    //         console.log('Checking user session...');
    //         setLoading(true)
    //         try {
    //             const userSession = await checkUserSession(setUser, navigate);
    //             if (!userSession) return;  // Stop if session is invalid
    //         } finally {
    //             setLoading(false)
    //         }
    //     };

    //     checkSession();  // Run session check only once on mount
    // }, []);

    useEffect(() => {
        const fetchInitialMovies = async () => {

            setLoadingComponent(true)
                if (currentPage === 1 && searchQuery.length > 0) {
                    setMovies([]);  // Reset movies for the first page
                }
                fetchMovies(searchQuery, currentPage, infiniteScroll)
                .then(() => setLoadingComponent(false))
                .catch((error) => {
                    setLoadingComponent(false);
                });
        };

        fetchInitialMovies();
    }, [currentPage, searchQuery, fetchMovies, setMovies, infiniteScroll]);

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

    const handleSearch = (query, page) => {
        if (!query) {
            alert("Please enter a search term");
            return;
        }
        setCurrentPage(1);
        // Navigate to the results page with the search query
        navigate(`/results/search?query=${query}&page=${page}`);
    }

    const handlePageChange = (newPage) => {
        console.log(currentPage, newPage, newPage <= totalPages)

        if (atResultsPage && newPage > 0 && !loading) {
            console.log(`2d validation Changing page to: ${newPage}`);
            setCurrentPage(newPage)
        }   
        
    };

    const classNames = `main-item montserrat-font ${!loading ? 'fade-in' : ''}`
    const { theme, toggleTheme } = useContext(ThemeContext);

    if (sessionLoading) {
        return <LoadingPage />
    }
    if (!sessionUser) {
        return null
    }

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
                    <a onClick={() => { navigate('/wishlist?page=1') }} className="btn btn-dark">
                        <svg xmlns="http://www.w3.org/2000/svg" width="30" height="23" fill="currentColor" className="bi bi-book" viewBox="0 0 16 16" style={{ color: 'rgb(210, 210, 210)' }}>
                            <path d="M1 2.828c.885-.37 2.154-.769 3.388-.893 1.33-.134 2.458.063 3.112.752v9.746c-.935-.53-2.12-.603-3.213-.493-1.18.12-2.37.461-3.287.811zm7.5-.141c.654-.689 1.782-.886 3.112-.752 1.234.124 2.503.523 3.388.893v9.923c-.918-.35-2.107-.692-3.287-.81-1.094-.111-2.278-.039-3.213.492zM8 1.783C7.015.936 5.587.81 4.287.94c-1.514.153-3.042.672-3.994 1.105A.5.5 0 0 0 0 2.5v11a.5.5 0 0 0 .707.455c.882-.4 2.303-.881 3.68-1.02 1.409-.142 2.59.087 3.223.877a.5.5 0 0 0 .78 0c.633-.79 1.814-1.019 3.222-.877 1.378.139 2.8.62 3.681 1.02A.5.5 0 0 0 16 13.5v-11a.5.5 0 0 0-.293-.455c-.952-.433-2.48-.952-3.994-1.105C10.413.809 8.985.936 8 1.783" />
                        </svg>
                    </a>

                </div>
            </div>
            <div className='content-container'>
                    <>
                        <MovieList
                            movies={movies}
                            loading={loadingComponent}
                            onWishlist={handleWishlist}
                            onPageChange={handlePageChange}
                            currentPage={currentPage}
                            totalPages={totalPages}
                            infiniteScroll={infiniteScroll}
                        />
                        {totalPages && currentPage <= totalPages && !infiniteScroll && totalPages > 1? (
                        <PaginationPanel
                            currentPage={currentPage}
                            totalPages={totalPages}
                            onPageChange={handlePageChange}
                        />
                    ) : null}
                    </>
            </div>
        </div>
    );
};

export default ResultsPage;
import React, { useState, useEffect, useContext, useCallback, useMemo } from 'react'
import { SearchBar } from '../utils/SearchBar'
import { MovieList } from './MovieList';
import { PaginationPanel } from '../utils/PaginationPanel';
import { useLocation, useNavigate } from 'react-router-dom';
import { useCheckUserSession } from './checkUserSession';
import { LoadingPage } from '../utils/LoadingPage';
import Switch from 'react-switch';
import { ThemeContext } from '../App';
import { useToast } from '../utils/ToastMessage';
import '../styles/Main.css';
import { useFetchMovies } from '../hooks/useFetchMovies';
import { useWishlist } from '../hooks/useWishlist';

const WishlistPage = () => {

    const navigate = useNavigate();
    const location = useLocation();
    const queryParams = useMemo(() => new URLSearchParams(location.search), [location.search]);
    const searchQuery = queryParams.get('query') || "";
    const [loading, setLoading] = useState(false);
    const [loadingComponent, setLoadingComponent] = useState(true);
    const { showToast } = useToast();
    const [currentPage, setCurrentPage] = useState(1);
    const { movies, setMovies, totalPages, fetchMovies } = useFetchMovies();
    const { fetchWishlistStatuses, handleWishlist } = useWishlist(showToast, setMovies);
    // const [infiniteScroll, setInfiniteScroll] = useState(false);
    const atWishlistPage = window.location.pathname.includes("/wishlist");
    const { loading: sessionLoading, user: sessionUser } = useCheckUserSession();
    const { theme, toggleTheme, scrollMode, togglePageMode } = useContext(ThemeContext);

    useEffect(() => {
        // Reset state on mode switch
        setCurrentPage(1);
        setMovies([]);
    }, [scrollMode]); 

    useEffect(() => {
        const fetchInitialMovies = () => {

            setLoadingComponent(true);
            if (currentPage === 1 && searchQuery.length > 0) {
                setMovies([]);  // Reset movies for the first page
            }

            fetchMovies(searchQuery, currentPage, scrollMode)
                .then(() => setLoadingComponent(false))
                .catch((error) => {
                    setLoadingComponent(false);
                });
        };

        fetchInitialMovies();
    }, [currentPage, searchQuery, fetchMovies, setMovies, scrollMode]);


    const handleSearch = useCallback((query, page) => {
        if (!query) {   
            navigate(`/wishlist?page=1`);
        }

        setCurrentPage(1)
        navigate(`/wishlist/search?query=${query}&page=${page}`)
    }, [navigate]);

    const handlePageChange = (newPage) => {

        if (atWishlistPage && newPage > 0 && !loading) {
            // console.log(`handlePagechange => Changing to page: ${newPage}`);
            setCurrentPage(newPage)

            if (!scrollMode) {
                navigate(`/wishlist?page=${newPage}`);

                if (searchQuery) {
                    navigate(`/wishlist/search?query=${searchQuery}&page=${newPage}`)
                }
            } 
            else {
                navigate(`/wishlist?page=1`);
            }
        } 

    };

    const classNames = `main-item ${!loading ? 'fade-in' : ''}`

    // if (sessionLoading && totalPages === 1 && scrollMode) {
    //     return <LoadingPage />
    // }   

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

                <Switch
                    onColor="#333130"
                    offColor="#333130"
                    checkedIcon={<span className="toggle-scroll-mode" role="img" aria-label="sound-on">page</span>}
                    uncheckedIcon={<span className="toggle-scroll-mode" role="img" aria-label="sound-off">scroll</span>}

                    className='switch' onChange={togglePageMode} checked={!scrollMode} />
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

                <>
                    <MovieList
                        movies={movies}
                        loading={loadingComponent}
                        onWishlist={handleWishlist}
                        onPageChange={handlePageChange}
                        currentPage={currentPage}
                        totalPages={totalPages}
                        infiniteScroll={scrollMode}
                    />
                    {totalPages && currentPage <= totalPages && !loadingComponent && totalPages > 1 && !scrollMode? (
                        <PaginationPanel
                            currentPage={currentPage}
                            totalPages={totalPages}
                            onPageChange={handlePageChange}
                        />
                    ) : null}
                </>

            </div>
        </div>
    )
}

export default WishlistPage
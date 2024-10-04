import React, { useState, useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { SearchBar } from './SearchBar';
import '../Main.css';
import { checkUserSession } from './checkUserSession';
import { LoadingPage } from './utils/LoadingPage';
import Switch from 'react-switch'
import { ThemeContext } from '../App'; // import the context

function Homepage() {

    const navigate = useNavigate();
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        checkUserSession(setLoading, setUser, navigate);
    }, [setLoading, setUser, navigate]);

    const handleSearch = async (query) => {

        if (!query) {
            alert("Please enter a search term");
            return;
        }

        const response = await fetch('http://localhost:5000/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include',
            body: JSON.stringify({ search: query })
        });

        if (response.status === 401) {
            console.log('Passed through')
            navigate('/login');
        }

        const result = await response.json();

        if (result.redirect) {
            console.log(result)
            navigate(`/results/search?query=${query}&page=1`)
        } else {
            // Handle any other response from backend
            console.error("error in search", result)
        }
    }

    // const onLogout = async () => {
    //     const response = await fetch('http://localhost:5000/logout', {
    //         method: "POST",
    //         credentials: "include"
    //     });

    //     if (response.ok) {
    //         navigate("/login");
    //     } else {
    //         console.error("Logout Failed")
    //     }
    // }

    const classNames = `main-item ${!loading ? 'fade-in' : ''}`
    const { theme, toggleTheme } = useContext(ThemeContext);

    if (loading) {
        return <LoadingPage />
    }

    if (!user) {
        return null;  // Optionally render nothing if not logged in
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

            <div className="button-container sub-container">

                {/* <div className='button-group'> */}
                    <SearchBar onSearch={handleSearch} />

                    <div class="side-buttons ms-3 mb-3">
                        <input onClick={() => { navigate('/logout') }} class="btn btn-outline-dark" name="logout" id="logout" type="submit" value="Log Out" />
                        <a onClick={() => { navigate('/wishlist') }} class="btn btn-dark">
                            <svg xmlns="http://www.w3.org/2000/svg" width="30" height="23" fill="currentColor" class="bi bi-book" viewBox="0 0 16 16" style={{ color: 'rgb(210, 210, 210)' }}>
                                <path d="M1 2.828c.885-.37 2.154-.769 3.388-.893 1.33-.134 2.458.063 3.112.752v9.746c-.935-.53-2.12-.603-3.213-.493-1.18.12-2.37.461-3.287.811zm7.5-.141c.654-.689 1.782-.886 3.112-.752 1.234.124 2.503.523 3.388.893v9.923c-.918-.35-2.107-.692-3.287-.81-1.094-.111-2.278-.039-3.213.492zM8 1.783C7.015.936 5.587.81 4.287.94c-1.514.153-3.042.672-3.994 1.105A.5.5 0 0 0 0 2.5v11a.5.5 0 0 0 .707.455c.882-.4 2.303-.881 3.68-1.02 1.409-.142 2.59.087 3.223.877a.5.5 0 0 0 .78 0c.633-.79 1.814-1.019 3.222-.877 1.378.139 2.8.62 3.681 1.02A.5.5 0 0 0 16 13.5v-11a.5.5 0 0 0-.293-.455c-.952-.433-2.48-.952-3.994-1.105C10.413.809 8.985.936 8 1.783" />
                            </svg>
                        </a>



                    {/* </div> */}

                </div>

            </div>

        </div>
    )
};

export default Homepage
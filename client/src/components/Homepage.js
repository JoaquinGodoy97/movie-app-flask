import React, { useState, useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { SearchBar } from '../utils/SearchBar';
import { useCheckUserSession } from './checkUserSession';
import { LoadingPage } from '../utils/LoadingPage';
import Switch from 'react-switch'
import { ThemeContext } from '../App';
import '../styles/Main.css';
import { AdminPanel } from '../utils/adminPanel';

function Homepage() {

    const navigate = useNavigate();
    const [user, setUser] = useState(null);
    const [adminStatus, setAdminStatus] = useState(false)
    const [loading, setLoading] = useState(false);
    const { loading: sessionLoading, user: sessionUser } = useCheckUserSession();

    // useEffect(() => {

    //     if (!sessionUser) return null

    // //     }
    // }, [sessionUser]);

    const handleSearch = async (query) => {

        if (!query) {
            alert("Please enter a search term");
            return;
        }

        setLoading(true)
        try {
            const apiBaseUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000';
            const token = localStorage.getItem('token');
            const response = await fetch(`${apiBaseUrl}/search`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
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
            setUser(result.username)
            

            if (result.redirect) {
                navigate(`/results/search?query=${query}&page=1`)
            } else {
                console.error("error in search", result)
            }
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => { 
        const storedStatus = localStorage.getItem('adminStatus') === 'true'; 
        setAdminStatus(storedStatus); 
    }, [])


    useEffect(() => {

        if(adminStatus){
            console.log(adminStatus, "Log the status of admin")
        } else {
            console.log(adminStatus, "Admin status is false.")
        }

    }, [adminStatus])

    const classNames = `main-item ${!loading ? 'fade-in' : ''}`
    const { theme, toggleTheme } = useContext(ThemeContext);

    if (sessionLoading) {
        return <LoadingPage />
    }
    if (!sessionUser) {
        return null
    }

    // if (!user) {
    //     return null; 
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

            <div className="button-container sub-container">

                {/* <div className='button-group'> */}
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

            {
            adminStatus ? 

            <AdminPanel/> : null }

        </div>
    )
};

export default Homepage
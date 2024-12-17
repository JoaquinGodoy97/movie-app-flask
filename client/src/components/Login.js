import React, { useState, useEffect, useContext } from 'react'
import { useNavigate } from 'react-router-dom'
import Switch from 'react-switch';
import { ThemeContext } from '../App';
import { useToast } from '../utils/ToastMessage';
import { isLoggedIn } from './checkUserSession';
import { LoadingPage } from '../utils/LoadingPage';
import '../styles/Login.css'

function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false); // I changed the state so It's not loading constantly
    const { showToast } = useToast();
    // const [data, setData] = useState('');

    useEffect(() => {

        const token = localStorage.getItem('token');
        if (!token) {
            // console.log('No token found, redirecting to login.');
            // showToast("Session expired.")
            navigate("/login")
            return;
        }

        const fetchData = async () => {
            setLoading(true)
            
            const apiBaseUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000';
            const options = {
                method: "GET",
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                credentials: 'include',
            };
            try {
                const response = await fetch(apiBaseUrl, options);
                const data = await response.json();

                if (response.status === 401) {
                    // If the token is invalid or expired, remove it and redirect to login
                    localStorage.removeItem('token');
                    navigate('/login');
                    return;
                }

            } catch (error) {
                console.log('Error fetching data:', error);
            } finally {
                setLoading(false)
            }
        };

        if (isLoggedIn) {
            setLoading(true)

            try {
                navigate('/search')
                showToast('Already logged in.')
            } catch {
                console.log("Failed to check if it's logged in")
            }
            finally {
                setLoading(false)
            }
        }

        fetchData();  // Call the async function

    }, [navigate]);

    const onSubmit = async (e) => {
        setLoading(true)

        e.preventDefault();

        const loginData = { username, password };


        const apiBaseUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000';
        console.log(apiBaseUrl)
        const url = `${apiBaseUrl}/login`;
        const options = {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            credentials: 'include',
            body: JSON.stringify(loginData)
        };

        try {
            const response = await fetch(url, options);
            const data = await response.json();

            if (response.ok) {

                localStorage.setItem('token', data.token)
                localStorage.setItem('currentUserId', data.user_id)

                if (data.adminStatus === 1){
                    localStorage.setItem('adminStatus', 'true')
                } else {
                    localStorage.setItem('adminStatus', 'false')
                }

                if (data.token) {
                    
                    showToast(data.message)
                    navigate(data.redirect) // Home page

                } else {
                    // console.log('Login failed:', data.message);
                    showToast(data.message)
                }

            } else {
                showToast(data.message);
                }
        } catch (error) {
            console.error("Error submitting form:", error);
        } finally {
            setLoading(false)
        }
    };

    const { theme, toggleTheme } = useContext(ThemeContext); // access theme and toggleTheme

    if (loading) {
        return <LoadingPage />
    }

    return (


        <div className="main-item montserrat-font">
            <nav className='nav-theme'>
                <Switch
                    onColor="#f5f490"
                    offColor="#333130"
                    checkedIcon={<span className="toggle-theme-mode" role="img" aria-label="sound-on">⛅</span>}
                    uncheckedIcon={<span className="toggle-theme-mode" role="img" aria-label="sound-off">🌘</span>}
                    className='switch' onChange={toggleTheme} checked={theme === 'dark'} />

            </nav>
            <div className="button-container login-element">
                <form method="POST" onSubmit={onSubmit}>
                    <div className="fields">
                        <label htmlFor="username" className="form-label">Username</label>
                        <input
                            type="text"
                            className="form-control"
                            value={username}
                            id="username"
                            name="username"
                            autoComplete="given-name"
                            onChange={(e) => setUsername(e.target.value)}
                        />
                    </div>

                    <div className="fields">
                        <label htmlFor="password" className="form-label">Password</label>
                        <input
                            type="password"
                            className="form-control"
                            value={password}
                            id="password"
                            name="password"
                            onChange={(e) => setPassword(e.target.value)}
                        />
                    </div>

                    <button name="login_submit" type="submit" className="btn btn-dark login-submit">Submit</button>


                </form>

            </div>

        </div>

    );
}

export default Login
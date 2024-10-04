import React, { useState, useEffect, useContext } from 'react'
import { useNavigate } from 'react-router-dom'
import '../Login.css'
import Switch from 'react-switch';
import { ThemeContext } from '../App'; // import the context

function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();
    const [data, setData] = useState('');

    // Check if the user is logged in when the component mounts
    useEffect(() => {

        fetch("http://localhost:5000") // "/" redirects "/login" 5000 (Flask) / 3000 (React)
            .then(res => res.json())
            .then(data => {
                setData(data);
                console.log(data)
                // if (!data.logged_in){
                navigate('/login')
                // }
            })
            .catch(error => console.error("Error fetching data:", error));

    }, [navigate]);

    // Handle form submission
    const onSubmit = async (e) => {
        e.preventDefault();

        const loginData = { username, password };

        const url = "http://localhost:5000/login";
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
            const result = await response.json();

            if (result.error) {
                navigate(result.redirect);
            }

            if (response.ok) {

                alert(result.message)
                navigate(result.redirect) // Home page 

            } else {
                alert(result.error);
            }
        } catch (error) {
            console.error("Error submitting form:", error);
        }
    };

    const { theme, toggleTheme } = useContext(ThemeContext); // access theme and toggleTheme

    return (
        <div className="login-element montserrat-font">
            <nav className='nav-theme'>
                <Switch
                    onColor="#f5f490"
                    offColor="#333130"
                    checkedIcon={<span className="toggle-theme-mode" role="img" aria-label="sound-on">⛅</span>}
                    uncheckedIcon={<span className="toggle-theme-mode" role="img" aria-label="sound-off">🌘</span>}

                    className='switch' onChange={toggleTheme} checked={theme === 'dark'} />
            </nav>
            <div className="button-container">
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
            {/* <SwitchThemeMode className='mt-4'/> */}

        </div>

    );
}

export default Login
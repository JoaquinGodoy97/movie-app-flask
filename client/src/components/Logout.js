import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

function Logout() {
    const navigate = useNavigate();

    useEffect(() => {
        const logout = async () => {
            const apiBaseUrl = window.location.hostname === 'localhost' ? 'http://localhost:5000' : process.env.REACT_APP_BACKEND_URL;
            const response = await fetch(`${apiBaseUrl}/logout`, {
                headers: {
                    "Content-type": "application/json"
                },
                method: 'POST',
                credentials: 'include'
            });

            const result = await response.json()

            if (response.ok) {
                localStorage.removeItem('token')
                navigate(result.redirect); // /login
            } else {
                alert(result.error);
            }
        };
        logout();
    }, [navigate]);

    return null;
}

export default Logout;
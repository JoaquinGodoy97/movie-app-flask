import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const fetchWithDelay = async () => {
    const apiBaseUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000';
    // await new Promise(resolve => setTimeout(resolve, 1000));  // Delay of 1 second
    return fetch(`${apiBaseUrl}/@me`, { headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
    },
    credentials: 'include' });
};

export const useCheckUserSession = () => {
    const [loading, setLoading] = useState(true);
    const [user, setUser] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const checkUserSession = async () => {
            try {
                const response = await fetchWithDelay();
                const data = await response.json();
                if (response.status === 401) {
                    navigate(data.redirect);
                } 
                else {
                    console.log("User data: ", data)
                    setUser(data);
                }
            } catch (error) {
                console.error('Error during user session check:', error);
                navigate('/login')
            } finally {
                setLoading(false)
            }
        };

        checkUserSession();
    }, [navigate])

    return { loading, user}
}

export const isLoggedIn = () => {
    const token = localStorage.getItem('token');
    // Check if token exists and optionally verify the token (you can use JWT decoding libraries)
    return !!token;  // Returns true if token exists, false otherwise
};
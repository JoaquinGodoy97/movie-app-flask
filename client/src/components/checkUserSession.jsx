import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useToast } from "../utils/ToastMessage";

const fetchWithDelay = async () => {
    const apiBaseUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000';
    // await new Promise(resolve => setTimeout(resolve, 1000));  // Delay of 1 second
    return fetch(`${apiBaseUrl}/@me`, { headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
        'Content-Type':'application/json'
    },
    credentials: 'include' });
};

export const useCheckUserSession = () => {
    const [loading, setLoading] = useState(true);
    const [user, setUser] = useState(null);
    const navigate = useNavigate();
    const { showToast } = useToast();

    useEffect(() => {

        const checkUserSession = async () => {

            const token = localStorage.getItem('token');
            if (!token) {
                navigate('/login');
                return;
            }
            
            try {
                const response = await fetchWithDelay();
                const data = await response.json();
                if (response.ok) {
                    setUser(data.username)
                } else {
                    localStorage.removeItem('token')
                    showToast(data.message)
                    navigate(data.redirect)
                }

            } catch (error) {
                console.error('Error during user session check:', error);
                navigate('/login')

            } finally {
                setLoading(false)
            }
        };
        checkUserSession(); 

        const interval = setInterval(checkUserSession, 300000); // 5 min , 1000 1 sec
        return () => clearInterval(interval); // Cleanup component unmount

    }, [navigate])

    return { loading, user}
}

export const isLoggedIn = () => {
    const token = localStorage.getItem('token');
    // Check if token exists and optionally verify the token (you can use JWT decoding libraries)
    return !!token;  // Returns true if token exists, false otherwise
};
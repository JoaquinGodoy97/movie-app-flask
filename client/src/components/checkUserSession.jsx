const fetchWithDelay = async () => {
    // await new Promise(resolve => setTimeout(resolve, 1000));  // Delay of 1 second
    return fetch("http://localhost:5000/@me", { headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
    },
    credentials: 'include' });
};

export const checkUserSession = async (setLoading, setUser, navigate) => {
    setLoading(true); 

    try {
        const response = await fetchWithDelay();
        console.log("Session check response:", response);
        const data = await response.json();

        if (response.status === 401) {
            console.warn("Unauthorized session. Redirecting...");
            navigate(data.redirect);
        } 
        else {
            console.log("User session valid:", data);
            setUser(data);
        }
    } catch (error) {
        console.error('Error during user session check:', error);
    } finally {
        setLoading(false);
    }
};

export const isLoggedIn = () => {
    const token = localStorage.getItem('token');
    // Check if token exists and optionally verify the token (you can use JWT decoding libraries)
    return !!token;  // Returns true if token exists, false otherwise
};
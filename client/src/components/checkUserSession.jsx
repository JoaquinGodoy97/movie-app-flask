
const fetchWithDelay = async () => {
    await new Promise(resolve => setTimeout(resolve, 1000));  // Delay of 1 second

    const token = localStorage.getItem('token');
    return fetch("http://localhost:5000/@me", {
        headers: {
            'Authorization': `Bearer ${token}`  // Send the token in Authorization header
        },
        credentials: 'include'
    });
};

export const checkUserSession = async (setLoading, setUser, navigate) => {
    setLoading(true);  // Ensure loading is true at the start

    try {
        const response = await fetchWithDelay();
        // console.log('Response status:', response.status); // Debugging response 
    
        // if (response.status === 401) {
        //     // Handle 401 Unauthorized explicitly
        //     navigate('/login');
        //     return;  // Exit function
        // }

        const data = await response.json();
        console.log("User data:", data)
        
        if (response.status === 401) {
            navigate('/login');
        } else {
            console.log("Whats,data?", data)
            setUser(data);
        }
    } catch (error) {
        console.error('Error during user session check:', error);
    } finally {
        setLoading(false);  // Ensure this only happens once everything else is done
    }
};
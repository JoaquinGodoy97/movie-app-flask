
const fetchWithDelay = async () => {
    await new Promise(resolve => setTimeout(resolve, 1000));  // Delay of 1 second
    return fetch("http://localhost:3000/@me", { credentials: 'include' });
};


export const checkUserSession = async (setLoading, setUser, navigate) => {
    setLoading(true);  // Ensure loading is true at the start

    try {

        const response = await fetchWithDelay();
        // const response = await fetch("http://localhost:3000/@me", {
        //     credentials: 'include'
        // });

        
        const data = await response.json();

        if (data.error === "Unauthorised") {
            navigate('/login');
        } else {
            setUser(data);
        }
    } catch (error) {
        console.error("No response ", error);
    } finally {
        // Simulate a delay to test loading
        setTimeout(() => {
            setLoading(false);  // Stop loading after delay
        }, 2000);  // Add 2 seconds delay
    }
};
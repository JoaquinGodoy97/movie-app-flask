export async function checkSession() {

    const response = await fetch('http://localhost:5000/check_session', {
        credentials: 'include'  // Include credentials for session management
    });

    return await response.json();
}
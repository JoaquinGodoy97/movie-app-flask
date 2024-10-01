import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { SearchBar } from './SearchBar';

function Homepage() {

    const navigate = useNavigate();
    const [user, setUser] = useState("");
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchUser = async () => {

            try {
                const response = await fetch("http://localhost:3000/@me", {
                    credentials: 'include'
                });
                const data = await response.json();  // Parse the JSON from the response
                setUser(data);  // Set the user state with the fetched data

                console.log(user)

                if (user.error === "Unauthorised") {
                    console.log("it passed")
                    navigate('/login');
                }

            } catch (error) {
                console.error("No response ", error);
            } finally {
                setLoading(false)
            }
        };

        fetchUser();  // Call the async function

    }, [user]);

    const handleSearch = async (query) => {

        if (!query) {
            alert("Please enter a search term");
            return;
        }

        const response = await fetch('http://localhost:5000/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            credentials: 'include',
            body: JSON.stringify({ search: query })
        });

        console.log(response)

        const result = await response.json();

        if (result.redirect) {
            console.log(result)
            navigate(`/results/search?query=${query}&page=1`)
        } else {
            // Handle any other response from backend
            console.error("error in search", result)
        }
    }

    // const onLogout = async () => {
    //     const response = await fetch('http://localhost:5000/logout', {
    //         method: "POST",
    //         credentials: "include"
    //     });

    //     if (response.ok) {
    //         navigate("/login");
    //     } else {
    //         console.error("Logout Failed")
    //     }
    // }
    if (loading) {
        return (
            <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', height: '70vh' }}>
                <h3>Loading . . .</h3>
            </div>)
    }

    return (

        <div className="main-item movie-search d-flex mt-5 mb-3">

            <div className="button-container">

                <SearchBar onSearch={handleSearch} />
                {/* <form className="form-floating" onSubmit={onSubmit}>

                <label htmlFor="search">Search Movies</label>

                <div className="button-container">

                    <div className="input-group search-group mb-3">
                        <input onChange={ (e) => setSearchTerm(e.target.value)} type="text" id="search" name="search" className="form-control" placeholder="Search" aria-label="Search" aria-describedby="basic-addon1" autoComplete="off"/>
                        <input className="btn btn-dark" type="submit" name="search_btn" id="search" value="Search"/>
                    </div>
                    
                    <div className="input-group search-group ms-3 mb-3">
                        <input className="btn btn-outline-dark" name="logout" id="logout" type="submit" value="Log Out"/>
                        <a href="#" className="btn btn-dark">
                            <svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" fill="currentColor" className="bi bi-book" viewBox="0 0 16 16" style={{ color: "rgb(210, 210, 210)" }}>
                                <path d="M1 2.828c.885-.37 2.154-.769 3.388-.893 1.33-.134 2.458.063 3.112.752v9.746c-.935-.53-2.12-.603-3.213-.493-1.18.12-2.37.461-3.287.811zm7.5-.141c.654-.689 1.782-.886 3.112-.752 1.234.124 2.503.523 3.388.893v9.923c-.918-.35-2.107-.692-3.287-.81-1.094-.111-2.278-.039-3.213.492zM8 1.783C7.015.936 5.587.81 4.287.94c-1.514.153-3.042.672-3.994 1.105A.5.5 0 0 0 0 2.5v11a.5.5 0 0 0 .707.455c.882-.4 2.303-.881 3.68-1.02 1.409-.142 2.59.087 3.223.877a.5.5 0 0 0 .78 0c.633-.79 1.814-1.019 3.222-.877 1.378.139 2.8.62 3.681 1.02A.5.5 0 0 0 16 13.5v-11a.5.5 0 0 0-.293-.455c-.952-.433-2.48-.952-3.994-1.105C10.413.809 8.985.936 8 1.783"/>
                            </svg>
                        </a>    
                    </div>
                </div>
                
                
            </form> */}

            </div>

        </div>
    )
};

export default Homepage
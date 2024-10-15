import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

export const SearchBar = ({ onSearch, initialQuery }) => {
    const [ searchQuery, setSearchQuery ] = useState(initialQuery || "");
    const navigate = useNavigate();
    
    const handleSubmit = (e) => {
        e.preventDefault();
        const atResultsPage = window.location.pathname.includes("/results/search")
        if(!searchQuery && atResultsPage){
            return navigate("/search")
        }
        if (!searchQuery.trim()) {

            alert("Please enter a search term");
            return;
        }

        onSearch(searchQuery, 1);  // Perform search and reset page to 1
    };

    return (
        <form onSubmit={handleSubmit}>
            {/* <label htmlFor="search">Search Movies</label> */}
            <div className="input-group mb-3 search-bar">
                <input
                    type="text"
                    id="search"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="form-control"
                    placeholder="Search"
                />
                <button type="submit" className="btn btn-dark search-btn">Search</button>
            </div>
        </form>
    )

};

// export default SearchBar;
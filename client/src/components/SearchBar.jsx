import React, { useState } from 'react';
// import { useNavigate } from 'react-router-dom';

const SearchBar = ({ onSearch, currentPage, totalPages, initialQuery }) => {
    const [ searchQuery, setSearchQuery ] = useState(initialQuery || "");
    // const navigate = useNavigate();
    
    const handleSubmit = (e) => {
        e.preventDefault();
        if (!searchQuery.trim()) {
            alert("Please enter a search term");
            return;
        }

        onSearch(searchQuery, 1);  // Perform search and reset page to 1
    };

    return (
        <form onSubmit={handleSubmit}>
            <label htmlFor="search">Search Movies</label>
            <div className="input-group mb-3">
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

export default SearchBar;
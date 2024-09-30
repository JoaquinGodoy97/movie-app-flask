import React from 'react'

const PaginationPanel = ({ currentPage, totalPages, onPageChange}) => {

    return (
        <div className="pagination-controls">
            <button
                className="btn btn-primary prev-btn"
                disabled={currentPage === 1}
                onClick={() => onPageChange(currentPage - 1)}  // Use separate handler for Prev button
                type="submit"
            >
                Prev
            </button>
            <button
                className="btn btn-primary next-btn"
                disabled={currentPage === totalPages}
                onClick={() => onPageChange(currentPage + 1)}  // Use separate handler for Next button
                type="submit"
            >   
                Next
            </button>
        </div>
    )
};

export default PaginationPanel

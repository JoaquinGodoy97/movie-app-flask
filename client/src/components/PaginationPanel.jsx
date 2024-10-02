import React from 'react'
import { Button } from 'react-bootstrap'

export const PaginationPanel = ({ currentPage, totalPages, onPageChange}) => {

    return (
        <div className="pagination-controls mb-3">
            <Button
                variant="dark"
                className="btn btn-primary prev-btn m-2"
                disabled={currentPage === 1}
                onClick={() => onPageChange(currentPage - 1)}  // Use separate handler for Prev button
                type="submit"
            >
                Prev
            </Button>
            <Button
                variant="dark"
                className="btn btn-primary next-btn"
                disabled={currentPage === totalPages}
                onClick={() => onPageChange(currentPage + 1)}  // Use separate handler for Next button
                type="submit"
            >   
                Next
            </Button>
        </div>
    )
};

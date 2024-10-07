import React from 'react'
import Pagination from 'react-bootstrap/Pagination';

export const PaginationPanel = ({ currentPage, totalPages, onPageChange }) => {

    let active = currentPage
    const items = []

    function range(start, end) {
        return Array.from({ length: end - start + 1 }, (_, i) => start + i);
    }
    
    // function numberRange(start, end) {
    //     console.log(`Start number: ${start}, End number: ${end}`);
    //     return range(start, end);
    // }

    const layoutPaginationItems = () => {
        const items = [];
        const startPage = Math.max(2, currentPage - 1);
        const endPage = Math.min(totalPages - 1, currentPage + 1);
    
        // Always show the first page
        items.push(
            <Pagination.Item key={1} active={currentPage === 1} onClick={() => onPageChange(1)}>
                1
            </Pagination.Item>
        );
    
        // Insert ellipsis if there's a gap between page 1 and startPage
        if (startPage > 2) {
            items.push(<Pagination.Ellipsis key="start-ellipsis" />);
        }
    
        // Show pages around the current page
        for (let number = startPage; number <= endPage; number++) {
            items.push(
                <Pagination.Item key={number} active={number === currentPage} onClick={() => onPageChange(number)}>
                    {number}
                </Pagination.Item>
            );
        }
    
        // Insert ellipsis if there's a gap between endPage and the last page
        if (endPage < totalPages - 1) {
            items.push(<Pagination.Ellipsis key="end-ellipsis" />);
        }
    
        // Always show the last page
        items.push(
            <Pagination.Item key={totalPages} active={currentPage === totalPages} onClick={() => onPageChange(totalPages)}>
                {totalPages}
            </Pagination.Item>
        );
    
        return items;
    };
    
    return (
        <Pagination className='pagination-group' disabled={totalPages <= 1}>
            {/* <Pagination.First onClick={()=> onPageChange(1)} disabled={currentPage === 1}/> */}

            {  currentPage === 1 ? 
            null :
            <Pagination.Prev onClick={()=> onPageChange(currentPage - 1)} disabled={currentPage === 1}/>
            }
            

            <span className='mx-2'>
            <Pagination disabled={currentPage === 1 || currentPage === totalPages}>{layoutPaginationItems()}</Pagination>
            </span>

            {  currentPage === totalPages ? 
            null :
            <Pagination.Next onClick={()=> onPageChange(currentPage + 1)} disabled={currentPage === totalPages}/>
            }
            
            {/* <Pagination.Last onClick={()=> onPageChange(totalPages)} disabled={currentPage === totalPages}/> */}
            {/* <Pagination size="lg">{items}</Pagination> */}
            {/* <br /> */}

            {/* <Pagination size="sm">{items}</Pagination> */}
        </Pagination>
    );

}

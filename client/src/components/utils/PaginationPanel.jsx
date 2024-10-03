import React from 'react'
import Pagination from 'react-bootstrap/Pagination';

export const PaginationPanel = ({ currentPage, totalPages, onPageChange }) => {

    let active = currentPage
    const items = []

    const middleNumber = Math.floor(totalPages / 2);
    
    function range(start, end) {
        return Array.from({ length: end - start + 1 }, (_, i) => start + i);
    }
    
    function numberRange(start, end) {
        console.log(`Start number: ${start}, End number: ${end}`);
        return range(start, end);
    }
    const startNumber = middleNumber - 1;
    const endNumber = middleNumber + 1;
    const finalPages = [1, startNumber, middleNumber, endNumber, totalPages]
    
    for (let number = 1; number <= totalPages; number++) {
            
        if (finalPages.includes(number) || totalPages <= 10){
            items.push(
                <Pagination.Item key={number} active={number === active} onClick={() => onPageChange(number)}>
                    {number}
                </Pagination.Item>,
            );
        } else {
            if (finalPages.includes(number - 1) && !finalPages.includes(number))
            items.push(
                <Pagination.Ellipsis />
            )
        }
    
    }
    return (
        <Pagination disabled={totalPages <= 1}>
            <Pagination.First onClick={()=> onPageChange(1)} disabled={currentPage === 1}/>
            <Pagination.Prev onClick={()=> onPageChange(currentPage - 1)} disabled={currentPage === 1}/>

            <span className='mx-2'>
            <Pagination disabled={currentPage === 1 || currentPage === totalPages}>{items}</Pagination>
            </span>
            
            <Pagination.Next onClick={()=> onPageChange(currentPage + 1)} disabled={currentPage === totalPages}/>
            <Pagination.Last onClick={()=> onPageChange(totalPages)} disabled={currentPage === totalPages}/>
            {/* <Pagination size="lg">{items}</Pagination> */}
            {/* <br /> */}

            {/* <Pagination size="sm">{items}</Pagination> */}
        </Pagination>
    );

}

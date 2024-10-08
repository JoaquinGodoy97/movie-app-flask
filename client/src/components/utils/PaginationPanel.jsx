import React from 'react'
import Pagination from 'react-bootstrap/Pagination';

export const PaginationPanel = ({ currentPage, totalPages, onPageChange }) => {

    function range(start, end) {
        return Array.from({ length: end - start + 1 }, (_, i) => start + i);
    }

    const layoutPaginationItems = () => {
        const items = [];
        const fpages = range(currentPage, currentPage + 2);
        const lpages = range(totalPages - 3, totalPages);
        const elipsis = null;
    
        const layoutPaginationItems = () => {
            if (lpages[0] > fpages[2]) {
                let layout = fpages.concat(elipsis).concat(lpages);
                return layout;
            } 
            
            else {
                return [...fpages, ...lpages];  // Ensure it returns an array even if the condition isn't met
            }
        };
    
        const layout = layoutPaginationItems();
    
        console.log("layout:", layout + " and total pages", totalPages);
        
        if (totalPages > 1) {
            for (let number = currentPage; number <= totalPages; number++) {
                if (totalPages <= 10) {
                    items.push(
                        <Pagination.Item key={number} active={number === currentPage} onClick={() => onPageChange(number)}>
                            {number}
                        </Pagination.Item>
                    );
                }
                
                else if (layout.includes(number)) {
                    items.push(
                        <Pagination.Item key={number} active={number === currentPage} onClick={() => onPageChange(number)}>
                            {number}
                        </Pagination.Item>
                    );
                } else if (layout.includes(null) && number !== null) {
                    items.push(<Pagination.Ellipsis key="end-ellipsis" />);
                    number = lpages[0];
                }
            }
        }
        
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

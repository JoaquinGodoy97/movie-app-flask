import Pagination from 'react-bootstrap/Pagination';

export const PaginationPanel = ({ currentPage, totalPages, onPageChange }) => {

    function range(start, end) {
        return Array.from({ length: end - start + 1 }, (_, i) => start + i);
    }

    const layoutPaginationItems = () => {
        const items = [];
    
        // Check if total pages is less than or equal to 10
        if (totalPages <= 10) {
            // Display all pages when total pages are less than or equal to 10
            for (let number = 1; number <= totalPages; number++) {
                items.push(
                    <Pagination.Item key={number} active={number === currentPage} onClick={() => onPageChange(number)}>
                        {number}
                    </Pagination.Item>
                );
            }
        } else {
            // Logic for when there are more than 10 pages
            const fpages = range(currentPage, currentPage + 2);
            const lpages = range(totalPages - 2, totalPages);
            const elipsis = null;
    
            const layout = fpages.concat(lpages[0] > fpages[2] ? [elipsis] : []).concat(lpages);
    
            // console.log("layout:", layout, "and total pages", totalPages);
    
            for (let number = currentPage; number <= totalPages; number++) {
                if (layout.includes(number)) {
                    items.push(
                        <Pagination.Item key={number} active={number === currentPage} onClick={() => onPageChange(number)}>
                            {number}
                        </Pagination.Item>
                    );
                } else if (layout.includes(null)) {
                    items.push(<Pagination.Ellipsis key="end-ellipsis" />);
                    number = lpages[0] - 1; // Jump to the first page in lpages after the ellipsis
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

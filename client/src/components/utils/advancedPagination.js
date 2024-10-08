const layoutPaginationItems = () => {
    const items = [];
    const startPage = Math.max(2, currentPage - 1);
    const endPage = Math.min(totalPages - 1, currentPage + 1);

    console.log(totalPages)

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
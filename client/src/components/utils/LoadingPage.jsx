
import React from 'react';
import Spinner from 'react-bootstrap/Spinner';

export const LoadingPage = () => {

        return (
            <div style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', height: '70vh' }}>
                {/* <h3>Loading . . .</h3> */}
                    <Spinner animation="border" variant="dark" role="status">
                        {/* <span className="visually-hidden">Loading...</span> */}
                    </Spinner>
            </div>
            
            );

}
import Button from 'react-bootstrap/Button';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import Tooltip from 'react-bootstrap/Tooltip';
import React, { memo } from 'react';

export const ToggleOverview = ( {overview} ) => {
    const renderTooltip = (props) => (
        <Tooltip id="button-tooltip" {...props}>
            {overview}
        </Tooltip>
    );

    return (
        <OverlayTrigger
            placement="right"
            delay={{ show: 0, hide: 100 }}
            overlay={renderTooltip}
        >
            <Button variant="secondary">More info</Button>
        </OverlayTrigger>
    );
};

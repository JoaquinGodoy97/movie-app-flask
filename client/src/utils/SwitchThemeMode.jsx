import React, { useState } from "react";
import Switch from "react-switch";

const SwitchThemeMode = () => {
    const [checked, setChecked] = useState(false);

    const handleChange = (nextChecked) => {
        setChecked(nextChecked);
    };

    return (
        <label>
            <Switch 
            id="pagination-buttons"
            onColor="#f5f490"
            offColor="#333130"
            checkedIcon={<span role="img" aria-label="sound-on">⛅</span>}
            uncheckedIcon={<span role="img" aria-label="sound-off">⛅🌘</span>}
            
            className="mt-4" onChange={handleChange} checked={checked} />
        </label>
    );
};

export default SwitchThemeMode;

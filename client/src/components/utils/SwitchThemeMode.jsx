import React, { useState } from "react";
import Switch from "react-switch";

const SwitchThemeMode = () => {
    const [checked, setChecked] = useState(false);

    const handleChange = (nextChecked) => {
        setChecked(nextChecked);
    };

    return (
        <label>
            <Switch className="mt-4" onChange={handleChange} checked={checked} />
        </label>
    );
};

export default SwitchThemeMode;

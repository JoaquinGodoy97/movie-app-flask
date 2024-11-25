import { useState } from "react"
import { createContext } from "react"

export const ThemeContext = createContext(null)

const [scrollMode, setScrollMode] = useState(true)

export const toggleTheme = () => {
    
    setScrollMode((current) => {
        const toggleScrollMode = current === true ? false : true;
        localStorage.setItem('scroll', pageMode);  // Save to localStorage
        return pageMode;
    });

}


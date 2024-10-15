import { useState } from "react"
import { createContext } from "react"

export const ThemeContext = createContext(null)

const [theme, setTheme] = useState('light')

export const toggleTheme = () => {
    
    setTheme((current) => {
        const newTheme = current === 'light' ? 'dark' : 'light';
        localStorage.setItem('theme', newTheme);  // Save to localStorage
        return newTheme;
    });

}


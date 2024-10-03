import { useState } from "react"
import { createContext } from "react"

export const ThemeContext = createContext(null)

const [theme, setTheme] = useState('light')

export const toggleTheme = () => {
    setTheme((current) => (current === 'light' ? 'dark' : 'light'))

    // return (
    //     <ThemeContext.Provider value={{ theme, setTheme}}>

    //     </ThemeContext.Provider>
    // )
}


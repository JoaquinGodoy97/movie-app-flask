import React, { useState, createContext } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './components/Login';
import Logout from './components/Logout';
import Homepage from './components/Homepage';
import ResultsPage from './components/ResultsPage';
import WishlistPage from './components/WishlistPage';
// import SwitchThemeMode from './components/utils/SwitchThemeMode';
import Switch from "react-switch";
import './App.css';

export const ThemeContext = createContext(null)

function App() {
  const [theme, setTheme] = useState('light')

  const toggleTheme = () => {
    setTheme((curr) => (curr === 'light' ? 'dark' : 'light'))
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme}}>

    <div className="App" id={theme}>
      {/* The theme switch */}
      {/* Your routing */}
      <Router>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/login" element={<Login />} />
          <Route path="/logout" element={<Logout />} />
          <Route path="/search" element={<Homepage />} />
          <Route path="/results/search" element={<ResultsPage />} />
          <Route path="/wishlist" element={<WishlistPage />} />
          <Route path="/wishlist/search" element={<WishlistPage />} />
        </Routes>
      </Router>
    </div>
    </ThemeContext.Provider>

  );
}

export default App;

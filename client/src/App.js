import React, { useState, createContext, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './components/Login';
import Logout from './components/Logout';
import Homepage from './components/Homepage';
import ResultsPage from './components/ResultsPage';
import WishlistPage from './components/WishlistPage';
import { ToastProvider } from './components/utils/ToastMessage';
import './App.css';

export const ThemeContext = createContext(null)

function App() {

  const [theme, setTheme] = useState(() => {
      return localStorage.getItem('theme') || 'light';
  });

  const toggleTheme = () => {
    
    setTheme((current) => {
        const newTheme = current === 'light' ? 'dark' : 'light';
        localStorage.setItem('theme', newTheme);  // Save to localStorage
        return newTheme;
    });

  }

  useEffect(() => {
    localStorage.setItem('theme', theme);
  }, [theme]);

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      <ToastProvider>

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
      </ToastProvider>
    </ThemeContext.Provider>

  );
}

export default App;

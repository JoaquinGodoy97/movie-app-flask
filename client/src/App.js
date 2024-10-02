import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import './App.css';
import Login from './components/Login';
import Logout from './components/Logout';
import Homepage from './components/Homepage';
import ResultsPage from './components/ResultsPage';
import WishlistPage from './components/WishlistPage';

function App() {
  return (
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
  );
}

export default App;

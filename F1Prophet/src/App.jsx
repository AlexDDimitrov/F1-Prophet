import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './Pages/home-page';
import DriverPage from './Pages/driverPage';
import DriverDetailPage from './Pages/DriverDetailPage'
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/drivers" element={<DriverPage />} />
        <Route path="/drivers/:driver_id" element={<DriverDetailPage />} />
      </Routes>
    </Router>
  )
}

export default App

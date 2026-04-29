import React from 'react';
import {BrowserRouter as Router, Routes, Route} from 'react-router-dom';
import HomePage from './Pages/home-page';
import DriverPage from './Pages/driverPage';
import DriverDetailPage from './Pages/DriverDetailPage'
import TeamPage from './Pages/TeamPage'
import LoginPage from './Pages/LoginPage'
import RegisterPage from './Pages/RegisterPage'
import PredictPage from './Pages/PredictPage';
import MyPredictionsPage from './Pages/MyPredictionsPage';
import AdminPage from './Pages/AdminPage';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/drivers" element={<DriverPage />} />
        <Route path="/drivers/:driver_id" element={<DriverDetailPage />} />
        <Route path="/teams" element={<TeamPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/predict" element={<PredictPage />} />
        <Route path="/my-predictions" element={<MyPredictionsPage/>} />
        <Route path="/admin" element={<AdminPage />} /> 
      </Routes>
    </Router>
  )
}

export default App

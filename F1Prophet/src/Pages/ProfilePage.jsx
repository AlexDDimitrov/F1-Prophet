import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './ProfilePage.css';

function ProfilePage() {
    const navigate = useNavigate();
    const [profile, setProfile] = useState(null);
    const [stats, setStats] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetchProfile();
        fetchStats();
    }, []);

    const fetchProfile = async () => {
        const token = localStorage.getItem('token');

        if (!token) {
            navigate('/login');
            return;
        }

        try {
            const response = await fetch('http://localhost:5000/api/users/profile', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!response.ok) {
                throw new Error('Failed to fetch profile');
            }

            const data = await response.json();
            setProfile(data);
        } catch (err) {
            console.error('Error fetching profile:', err);
            setError(err.message);
        }
    };

    const fetchStats = async () => {
        const token = localStorage.getItem('token');

        try {
            const response = await fetch('http://localhost:5000/api/users/stats', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!response.ok) {
                throw new Error('Failed to fetch stats');
            }

            const data = await response.json();
            setStats(data);
            setLoading(false);
        } catch (err) {
            console.error('Error fetching stats:', err);
            setError(err.message);
            setLoading(false);
        }
    };

    const formatDate = (dateString) => {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', { 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric' 
        });
    };

    const handleEditProfile = () => {
        console.log('Edit profile clicked');
    };

    if (loading) {
        return (
            <div className='profile-page'>
                <div className='loading'>Loading profile...</div>
            </div>
        );
    }

    if (error) {
        return (
            <div className='profile-page'>
                <div className='error'>Error: {error}</div>
            </div>
        );
    }

    if (!profile) {
        return (
            <div className='profile-page'>
                <div className='error'>Profile not found</div>
            </div>
        );
    }

    return (
        <div className='profile-page'>
            <button onClick={() => navigate('/')} className='profile-back-button'>
                Back to Home
            </button>

            <div className='profile-container'>
                <header className='profile-header'>
                    <h1 className='profile-title'>User Profile</h1>
                    <button onClick={handleEditProfile} className='edit-profile-button'>
                        Edit Profile
                    </button>
                </header>

                <div className='profile-content'>
                    <div className='profile-info-card'>
                        <h2 className='card-title'>Account Information</h2>
                        
                        <div className='info-row'>
                            <span className='info-label'>Username:</span>
                            <span className='info-value'>{profile.username}</span>
                        </div>

                        <div className='info-row'>
                            <span className='info-label'>Email:</span>
                            <span className='info-value'>{profile.email}</span>
                        </div>

                        <div className='info-row'>
                            <span className='info-label'>Member Since:</span>
                            <span className='info-value'>{formatDate(profile.created_at)}</span>
                        </div>

                        <div className='info-row'>
                            <span className='info-label'>Total Points:</span>
                            <span className='info-value highlight'>{profile.total_points}</span>
                        </div>

                        <div className='info-row'>
                            <span className='info-label'>Global Rank:</span>
                            <span className='info-value highlight'>#{profile.global_rank}</span>
                        </div>

                        <div className='info-row'>
                            <span className='info-label'>Predictions Made:</span>
                            <span className='info-value'>{profile.predictions_made}</span>
                        </div>
                    </div>

                    <div className='profile-stats-card'>
                        <h2 className='card-title'>Achievements</h2>

                        {stats && stats.best_prediction ? (
                            <>
                                <div className='achievement-section'>
                                    <h3 className='achievement-title'>Best Prediction</h3>
                                    <div className='achievement-details'>
                                        <div className='achievement-points'>
                                            {stats.best_prediction.points} points
                                        </div>
                                        <div className='achievement-race'>
                                            {stats.best_prediction.race_name}
                                        </div>
                                        <div className='achievement-location'>
                                            {stats.best_prediction.race_location}
                                        </div>
                                        <div className='achievement-date'>
                                            {formatDate(stats.best_prediction.race_date)}
                                        </div>
                                    </div>
                                </div>

                                <div className='achievement-section'>
                                    <h3 className='achievement-title'>Average Performance</h3>
                                    <div className='achievement-details'>
                                        <div className='achievement-average'>
                                            {stats.average_points} points per race
                                        </div>
                                        <div className='achievement-total'>
                                            <span>Based on {stats.total_completed} completed predictions</span>
                                        </div>
                                    </div>
                                </div>
                            </>
                        ) : (
                            <div className='no-achievements'>
                                <p>No completed predictions yet.</p>
                                <p>Make your first prediction to see your achievements!</p>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default ProfilePage;
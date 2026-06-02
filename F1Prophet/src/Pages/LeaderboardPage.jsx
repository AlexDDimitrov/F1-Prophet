import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import F1Loader from '../Components/F1Loader';
import './LeaderboardPage.css';

function LeaderboardPage() {
    const navigate = useNavigate();
    const [activeTab, setActiveTab] = useState('seasonal');
    const [leaderboard, setLeaderboard] = useState([]);
    const [currentUserRank, setCurrentUserRank] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    const currentYear = new Date().getFullYear();
    const currentMonth = new Date().getMonth() + 1;

    useEffect(() => {
        fetchLeaderboard();
    }, [activeTab]);

    const fetchLeaderboard = async () => {
        setLoading(true);
        setError(null);

        const token = localStorage.getItem('token');
        const headers = token ? { 'Authorization': `Bearer ${token}` } : {};

        let url = '';
        if (activeTab === 'monthly') {
            url = `http://localhost:5000/api/leaderboards/monthly/${currentYear}/${currentMonth}`;
        } else if (activeTab === 'seasonal') {
            url = `http://localhost:5000/api/leaderboards/seasonal/${currentYear}`;
        } else {
            url = 'http://localhost:5000/api/leaderboards/all-time';
        }

        try {
            const response = await fetch(url, { headers });

            if (!response.ok) {
                throw new Error('Failed to fetch leaderboard');
            }

            const data = await response.json();
            setLeaderboard(data.leaderboard);
            setCurrentUserRank(data.current_user_rank);
            setLoading(false);
        } catch (err) {
            console.error('Error fetching leaderboard:', err);
            setError(err.message);
            setLoading(false);
        }
    };

    const getRankIcon = (rank) => {
        if (rank === 1) return '№1';
        if (rank === 2) return '№2';
        if (rank === 3) return '№3';
        return `#${rank}`;
    };

    if (loading) {
        return (
            <div>                
                <div className='predict-page'>
                    <F1Loader message="Loading leaderboard..." />
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className='leaderboard-page'>
                <div className='error'>Error: {error}</div>
            </div>
        );
    }

    return (
        <div className='leaderboard-page'>
            <button onClick={() => navigate('/')} className='leaderboard-back-button'>
                ← Back to Home
            </button>

            <div className='leaderboard-container'>
                <header className='leaderboard-header'>
                    <h1 className='leaderboard-title'>Leaderboards</h1>
                    <p className='leaderboard-subtitle'>Top Predictors of F1 Prophet</p>
                </header>

                <div className='leaderboard-tabs'>
                    <button
                        className={`tab-button ${activeTab === 'monthly' ? 'active' : ''}`}
                        onClick={() => setActiveTab('monthly')}
                    >
                        Monthly
                    </button>
                    <button
                        className={`tab-button ${activeTab === 'seasonal' ? 'active' : ''}`}
                        onClick={() => setActiveTab('seasonal')}
                    >
                        Seasonal
                    </button>
                    <button
                        className={`tab-button ${activeTab === 'all-time' ? 'active' : ''}`}
                        onClick={() => setActiveTab('all-time')}
                    >
                        All-Time
                    </button>
                </div>

                {currentUserRank && (
                    <div className='user-rank-box'>
                        <span className='your-rank-label'>Your Rank:</span>
                        <span className='your-rank-value'>#{currentUserRank}</span>
                    </div>
                )}

                <div className='leaderboard-table'>
                    <div className='table-header'>
                        <div className='header-rank'>Rank</div>
                        <div className='header-username'>Username</div>
                        <div className='header-points'>Points</div>
                        <div className='header-predictions'>Predictions</div>
                    </div>

                    <div className='table-body'>
                        {leaderboard.map((entry) => (
                            <div
                                key={entry.user_id}
                                className={`table-row ${entry.is_current_user ? 'current-user' : ''}`}
                            >
                                <div className='row-rank'>
                                    <span className='rank-icon'>{getRankIcon(entry.rank)}</span>
                                </div>
                                <div className='row-username'>{entry.username}</div>
                                <div className='row-points'>{entry.total_points}</div>
                                <div className='row-predictions'>{entry.predictions_count}</div>
                            </div>
                        ))}
                    </div>
                    
                    {leaderboard.length === 0 && (
                        <div className='no-data'>
                            <p>No leaderboard data yet. Be the first to make predictions!</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}

export default LeaderboardPage;
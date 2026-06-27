import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import F1Loader from '../Components/F1Loader';
import './RaceCalendarPage.css';

function RaceCalendarPage() {
    const navigate = useNavigate();
    const [races, setRaces] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [currentYear, setCurrentYear] = useState(new Date().getFullYear());
    const [filterStatus, setFilterStatus] = useState('all');
    const [countdowns, setCountdowns] = useState({});

    const raceImageMap = {
        'Australian Grand Prix': 'albert_park.png',
        'Chinese Grand Prix': 'shangha.png',
        'Japanese Grand Prix': 'suzuka.png',
        'Miami Grand Prix': 'miami.png',
        'Canadian Grand Prix': 'canada.png',
        'Monaco Grand Prix': 'monaco.png',
        'Spanish Grand Prix (Barcelona)': 'barcelona.png',
        'Austrian Grand Prix': 'spielberg.png',
        'British Grand Prix': 'silverstone.png',
        'Belgian Grand Prix': 'spa.png',
        'Hungarian Grand Prix': 'budapest.png',
        'Dutch Grand Prix': 'zandvoort.png',
        'Italian Grand Prix': 'monza.png',
        'Spanish Grand Prix (Madrid)': 'madrid.png',
        'Azerbaijan Grand Prix': 'baku.png',
        'Singapore Grand Prix': 'singapore.png',
        'United States Grand Prix': 'austin.png',
        'Mexico City Grand Prix': 'mexico_city.png',
        'Brazilian Grand Prix': 'sao_paulo.png',
        'Las Vegas Grand Prix': 'las_vegas.png',
        'Qatar Grand Prix': 'lusail.png',
        'Abu Dhabi Grand Prix': 'abu_dhabi.png'
    };

    useEffect(() => {
        fetchRaces();
    }, [currentYear]);

    const fetchRaces = async () => {
        try {
            setLoading(true);
            const response = await fetch(`http://localhost:5000/api/races/race_calendar/${currentYear}`);

            if (!response.ok) {
                throw new Error('Failed to fetch races');
            }

            const data = await response.json();
            setRaces(data);
            setError(null);
            setLoading(false);
        } catch (err) {
            console.error('Error fetching races:', err);
            setError(err.message || 'Failed to load race calendar');
            setLoading(false);
        }
    };

    useEffect(() => {
        const interval = setInterval(() => {
            const newCountdowns = {};

            races.forEach(race => {
                const raceTime = new Date(race.race_date).getTime();
                const now = new Date().getTime();
                const diff = raceTime - now;

                if (diff > 0) {
                    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
                    const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
                    const seconds = Math.floor((diff % (1000 * 60)) / 1000);

                    newCountdowns[race.id] = { days, hours, minutes, seconds };
                } else {
                    newCountdowns[race.id] = null;
                }
            });

            setCountdowns(newCountdowns);
        }, 1000);

        return () => clearInterval(interval);
    }, [races]);

    const getStatusBadge = (status) => {
        const statusStyles = {
            'upcoming': { bg: '#0066FF', text: 'UPCOMING' },
            'active': { bg: '#FF9500', text: 'ACTIVE' },
            'completed': { bg: '#00AA00', text: 'COMPLETED' },
            'cancelled': { bg: '#AA0000', text: 'CANCELLED' }
        };

        const style = statusStyles[status] || statusStyles['upcoming'];
        return style;
    };

    const getBackgroundImage = (raceName) => {
        const imageName = raceImageMap[raceName] || 'default.png';
        return `/images/grand prix/${imageName}`;
    };

    const filteredRaces = races.filter(race => {
        if (filterStatus === 'all') return true;
        return race.status === filterStatus;
    });

    const sortedRaces = [...filteredRaces].sort((a, b) => {
        return a.round_number - b.round_number;
    });

    if (loading) {
        return (
            <div className='race-calendar-page'>
                <F1Loader message="Loading race calendar..." />
            </div>
        );
    }

    return (
        <div className='race-calendar-page'>
            <button onClick={() => navigate('/')} className='back-button'>
                ← Back to Home
            </button>

            <header className='calendar-header'>
                <h1 className='page-title'>F1 RACE CALENDAR</h1>
                <p className='page-subtitle'>2026 Season</p>
            </header>

            {error && (
                <div className='error-message'>
                    <p>{error}</p>
                </div>
            )}

            <div className='calendar-controls'>
                <div className='year-selector'>
                    <button 
                        className='year-btn'
                        onClick={() => setCurrentYear(currentYear - 1)}
                    >
                        ← {currentYear - 1}
                    </button>
                    <span className='current-year'>{currentYear}</span>
                    <button 
                        className='year-btn'
                        onClick={() => setCurrentYear(currentYear + 1)}
                    >
                        {currentYear + 1} →
                    </button>
                </div>

                <div className='filter-buttons'>
                    <button 
                        className={`filter-btn ${filterStatus === 'all' ? 'active' : ''}`}
                        onClick={() => setFilterStatus('all')}
                    >
                        All Races
                    </button>
                    <button 
                        className={`filter-btn ${filterStatus === 'upcoming' ? 'active' : ''}`}
                        onClick={() => setFilterStatus('upcoming')}
                    >
                        Upcoming
                    </button>
                    <button 
                        className={`filter-btn ${filterStatus === 'active' ? 'active' : ''}`}
                        onClick={() => setFilterStatus('active')}
                    >
                        Active
                    </button>
                    <button 
                        className={`filter-btn ${filterStatus === 'completed' ? 'active' : ''}`}
                        onClick={() => setFilterStatus('completed')}
                    >
                        Completed
                    </button>
                </div>
            </div>

            {!error && (<>
                <div className='races-grid'>
                    {sortedRaces.length === 0 ? (
                        <div className='no-races'>
                            <p>No races found for {currentYear}</p>
                        </div>
                    ) : (
                        sortedRaces.map((race) => (
                            <div 
                                key={race.id} 
                                className='race-card'
                            >
                                <div className='race-header'>
                                    <div className='race-round'>
                                        <span className='round-label'>Round</span>
                                        <span className='round-number'>{race.round_number}</span>
                                    </div>
                                    <div className={`status-badge`} style={{background: getStatusBadge(race.status).bg}}>
                                        {getStatusBadge(race.status).text}
                                    </div>
                                </div>

                                <div className='race-info'>
                                    <h2 className='race-name'>{race.name}</h2>
                                    <p className='race-location'>{race.location}</p>
                                </div>

                                <div className='race-details'>
                                    <div className='detail-item'>
                                        <span className='detail-label'>Race Date</span>
                                        <span className='detail-value'>
                                            {new Date(race.race_date).toLocaleDateString('en-US', {
                                                weekday: 'short',
                                                month: 'short',
                                                day: 'numeric',
                                                hour: '2-digit',
                                                minute: '2-digit'
                                            })}
                                        </span>
                                    </div>
                                    
                                    <div className='detail-item'>
                                        <span className='detail-label'>Prediction <br></br>Deadline</span>
                                        <span className='detail-value'>
                                            {new Date(race.deadline).toLocaleDateString('en-US', {
                                                weekday: 'short',
                                                month: 'short',
                                                day: 'numeric',
                                                hour: '2-digit',
                                                minute: '2-digit'
                                            })}
                                        </span>
                                    </div>
                                </div>

                                {countdowns[race.id]? (
                                    <div className='countdown'>
                                        <span className='countdown-label'>Starts in</span>
                                        <div className='countdown-values'>
                                            <div className='countdown-item'>
                                                <span className='countdown-number'>{countdowns[race.id].days}</span>
                                                <span className='countdown-unit'>days</span>
                                            </div>
                                            <div className='countdown-item'>
                                                <span className='countdown-number'>{countdowns[race.id].hours}</span>
                                                <span className='countdown-unit'>hrs</span>
                                            </div>
                                            <div className='countdown-item'>
                                                <span className='countdown-number'>{countdowns[race.id].minutes}</span>
                                                <span className='countdown-unit'>min</span>
                                            </div>
                                            <div className='countdown-item'>
                                                <span className='countdown-number'>{countdowns[race.id].seconds}</span>
                                                <span className='countdown-unit'>sec</span>
                                            </div>
                                        </div>
                                    </div>
                                ): <div className='countdown'>
                                    <span className='countdown-label'>Starts in</span>
                                    <div className='countdown-item'>
                                            <span className='countdown-number'>Deadline passed</span>
                                            <span className='countdown-unit'></span>
                                        </div>
                                </div>
                                }
                                <div className="track-image-container">
                                    <img
                                        src={getBackgroundImage(race.name)}
                                        alt={race.name}
                                        className="track-image"
                                    />
                                </div>
                            </div>
                        ))
                    )}
                </div>
            </>)}

            {error && (
                <div className='no-races'>
                    <p>No races found for {currentYear}</p>
                </div>
            )}

            <div className='bottom-action'>
                <button 
                    className='predict-btn-bottom'
                    onClick={() => navigate('/predict')}
                >
                    Make Prediction →
                </button>
            </div>
        </div>
    );
}

export default RaceCalendarPage;
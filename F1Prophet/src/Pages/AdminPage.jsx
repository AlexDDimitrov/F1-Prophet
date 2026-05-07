import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './AdminPage.css'
import '../Components/F1Loader'
import F1Loader from '../Components/F1Loader';

function AdminPage() {
    const navigate = useNavigate();
    const [races, setRaces] = useState([]);
    const [selectedRaceId, setSelectedRaceId] = useState('');
    const [race, setRace] = useState(null);
    const [drivers, setDrivers] = useState([]);
    const [results, setResults] = useState({});
    const [fastestLap, setFastestLap] = useState('');
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState('');

    useEffect(() => {
        const checkAdmin = async () => {
            const token = localStorage.getItem('token');
            if (!token) {
                navigate('/login');
                return;
            }

            try {
                const response = await fetch('http://localhost:5000/api/auth/me', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (response.ok) {
                    const user = await response.json();
                    if (!user.is_admin) {
                        navigate('/');
                    }
                } else {
                    navigate('/login');
                }
            } catch (err) {
                console.error('Error:', err);
                navigate('/login');
            }
        };

        const fetchData = async () => {
            try {
                const racesRes = await fetch('http://localhost:5000/api/races/all');
                if (racesRes.ok) {
                    const racesData = await racesRes.json();
                    setRaces(racesData);
                    
                    if (racesData.length > 0) {
                        setSelectedRaceId(racesData[0].id.toString());
                        setRace(racesData[0]);
                    }
                }

                const driversRes = await fetch('http://localhost:5000/api/drivers');
                if (driversRes.ok) {
                    const driversData = await driversRes.json();
                    setDrivers(driversData);
                    
                    const initialResults = {};
                    driversData.forEach(driver => {
                        initialResults[driver.driver_id] = {
                            position: null,
                            is_dnf: false
                        };
                    });
                    setResults(initialResults);
                }
            } catch (err) {
                console.error('Error fetching data:', err);
            }
        };

        checkAdmin();
        fetchData();
    }, [navigate]);

    const handleRaceChange = (e) => {
        const raceId = e.target.value;
        setSelectedRaceId(raceId);
        
        const selectedRace = races.find(r => r.status === 'upcoming' && r.id === Number(raceId));
        setRace(selectedRace);
        
        const resetResults = {};
        drivers.forEach(driver => {
            resetResults[driver.driver_id] = {
                position: null,
                is_dnf: false
            };
        });
        setResults(resetResults);
        setFastestLap('');
        setMessage('');
    };

    const handlePositionChange = (driverId, position) => {
        setResults(prev => ({
            ...prev,
            [driverId]: {
                ...prev[driverId],
                position: position ? parseInt(position) : null,
                is_dnf: false
            }
        }));
    };

    const handleDnfToggle = (driverId) => {
        setResults(prev => {
            const newDnf = !prev[driverId].is_dnf;
            return {
                ...prev,
                [driverId]: {
                    ...prev[driverId],
                    is_dnf: newDnf,
                    position: newDnf ? null : prev[driverId].position
                }
            };
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setMessage('');

        const token = localStorage.getItem('token');
        if (!token) {
            navigate('/login');
            return;
        }

        const actualResults = Object.entries(results)
            .filter(([_, result]) => result.position !== null || result.is_dnf)
            .map(([driverId, result]) => ({
                driver_id: driverId,
                position: result.position,
                is_dnf: result.is_dnf
            }));

        try {
            const response = await fetch(`http://localhost:5000/api/admin/calculate-points/${selectedRaceId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    actual_results: actualResults,
                    fastest_lap: fastestLap
                })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Failed to calculate points');
            }

            const data = await response.json();
            setMessage(`${data.message}`);
            
        } catch (err) {
            console.error('Error:', err);
            setMessage(`Error: ${err.message}`);
        } finally {
            setLoading(false);
        }
    };

    if (!race || drivers.length === 0) {
        return (
            <div className='admin-page'>
                <F1Loader message="Loading race data..."/>
            </div>
        );
    }

    return (
        <div className='admin-page'>
            <button onClick={() => navigate('/')} className='admin-back-button'>
                ← Back to Home
            </button>

            <div className='admin-container'>
                <header className='admin-header'>
                    <h1 className='admin-title'>Admin Panel</h1>
                    <p className='admin-subtitle'>Enter race results and calculate points</p>
                </header>

                <div className='admin-race-selector'>
                    <label htmlFor='race-select'>Select Race:</label>
                    <select
                        id='race-select'
                        value={selectedRaceId}
                        onChange={handleRaceChange}
                        className='admin-race-select'
                    >
                        {races.map((r) => (
                            <option key={r.id} value={r.id}>
                                Round {r.round_number} - {r.name} ({r.status})
                            </option>
                        ))}
                    </select>
                </div>

                <div className='admin-race-info'>
                    <h2>{race.name}</h2>
                    <p>{new Date(race.race_date).toLocaleDateString()}</p>
                    <span className={`admin-race-status ${race.status}`}>
                        {race.status}
                    </span>
                </div>

                {message && (
                    <div className={`admin-message ${message ? 'success' : 'error'}`}>
                        {message}
                    </div>
                )}

                <form onSubmit={handleSubmit} className='admin-form'>
                    <div className='admin-results-section'>
                        <h3>Race Results</h3>
                        <p className='admin-instruction'>Enter finishing positions or mark as DNF</p>
                        <div className='admin-results-grid'>
                            {drivers.map((driver) => (
                                <div key={driver.driver_id} className='admin-result-item'>
                                    <div className='admin-driver-info'>
                                        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
                                            <img 
                                                className='driver-image-small' 
                                                src={`/images/drivers/${driver.code}.png`} 
                                                alt={driver.full_name}
                                                onError={(e) => { e.target.style.display = 'none'; }}
                                            />
                                        </div>
                                        <span className='admin-driver-code'>{driver.code}</span>
                                        <span className='admin-driver-name'>{driver.full_name}</span>
                                    </div>

                                    <div className='admin-result-inputs'>
                                        <input
                                            type='number'
                                            min='1'
                                            max='22'
                                            placeholder='P#'
                                            value={results[driver.driver_id]?.position || ''}
                                            onChange={(e) => handlePositionChange(driver.driver_id, e.target.value)}
                                            disabled={results[driver.driver_id]?.is_dnf}
                                            className='admin-position-input'
                                        />

                                        <label className='admin-dnf-checkbox'>
                                            <input
                                                type='checkbox'
                                                checked={results[driver.driver_id]?.is_dnf || false}
                                                onChange={() => handleDnfToggle(driver.driver_id)}
                                            />
                                            <span>DNF</span>
                                        </label>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>

                    <div className='admin-fastest-lap-section'>
                        <h3>Fastest Lap</h3>
                        <select
                            value={fastestLap}
                            onChange={(e) => setFastestLap(e.target.value)}
                            className='admin-fastest-lap-select'
                            required
                        >
                            <option value=''>Select driver...</option>
                            {drivers.map((driver) => (
                                <option key={driver.driver_id} value={driver.driver_id}>
                                    {driver.code} - {driver.full_name}
                                </option>
                            ))}
                        </select>
                    </div>

                    <button
                        type='submit'
                        className='admin-calculate-button'
                        disabled={loading}
                    >
                        {loading ? 'Calculating...' : 'Calculate Points'}
                    </button>
                </form>

                <div className='admin-points-info'>
                    <h3>Points System:</h3>
                    <ul>
                        <li>&bull; Correct position: 10 pts</li>
                        <li>&bull; ±1 position: 5 pts</li>
                        <li>&bull; ±2 positions: 3 pts</li>
                        <li>&bull; Correct DNF: 5 pts</li>
                        <li>&bull; Correct fastest lap: +5 pts</li>
                    </ul>
                </div>
            </div>
        </div>
    );
}

export default AdminPage;
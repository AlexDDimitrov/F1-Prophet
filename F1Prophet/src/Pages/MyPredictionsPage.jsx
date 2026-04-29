import React, {useState, useEffect} from 'react';
import {useNavigate} from 'react-router-dom';
import F1Loader from '../Components/F1Loader';
import './MyPredictionPage.css'

function MyPredictionsPage() {
    const navigate = useNavigate();
    const [predictions, setPredictions] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [drivers, setDrivers] = useState({});

    useEffect(() => {
        const fetchData = async () => {
            const token = localStorage.getItem('token');
            
            if (!token) {
                navigate('/login');
                return;
            }

            try {
                const driversRes = await fetch('http://localhost:5000/api/drivers');
                if (driversRes.ok) {
                    const driversData = await driversRes.json();
                    const driversMap = {};
                    driversData.forEach(d => {
                        driversMap[d.driver_id] = d;
                    });
                    setDrivers(driversMap);
                }

                const predictionsRes = await fetch('http://localhost:5000/api/predictions/my', {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });

                if (!predictionsRes.ok) {
                    throw new Error('Failed to fetch predictions');
                }

                const predictionsData = await predictionsRes.json();
                setPredictions(predictionsData);
                setLoading(false);
            } catch (err){
                console.error('Error:', err);
                setError(err.message);
                setLoading(false);
            }
        };

        fetchData();
    }, [navigate]);

    if (loading) {
        return (
            <div>                
                <div className='predict-page'>
                    <F1Loader message="Loading predictions..." />
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className='my-predictions-page'>
                <div className='error'>Error: {error}</div>
            </div>
        );
    }

    return (
        <div className='my-predictions-page'>
            <button onClick={() => navigate('/predict')} className='my-back-button'>
                ← Back to Predict
            </button>

                <header className='my-page-header'>
                    <h1 className='my-page-title'>My Predictions</h1>
                    <p className='my-page-subtitle'>Your prediction history</p>
                </header>

                {predictions.length === 0 ? (
                    <div className='my-no-predictions'>
                        <p>You haven't made any predictions yet.</p>
                        <button onClick={() => navigate('/predict')} className='my-cta-button'>
                            Make Your First Prediction
                        </button>
                    </div>
                ) : (
                    <div className='my-predictions-list'>
                        {predictions.map((prediction) => (
                            <div key={prediction.id} className='my-prediction-card'>
                                <div className='my-prediction-header'>
                                    <h2 className='my-race-name'>{prediction.race_name}</h2>
                                    <span className={`my-race-status ${prediction.status}`}>
                                        {prediction.status}
                                    </span>
                                </div>

                                <div className='my-prediction-meta'>
                                    <span>{prediction.location}</span>
                                    <span>{new Date(prediction.race_date).toLocaleDateString()}</span>
                                    <span>Submitted: {new Date(prediction.submitted_at).toLocaleString()}</span>
                                </div>
                                {//To update: points earned
                                }
                                {prediction.points_earned !== null && (
                                    <div className='my-points-earned'>
                                        Points Earned: {prediction.points_earned}
                                    </div>
                                )}

                                <div className='my-predicted-positions'>
                                    <h3>Predicted Positions:</h3>
                                    <div className='my-positions-grid'>
                                        {prediction.positions
                                            .filter(p => !p.is_dnf)
                                            .map((pos) => (
                                                <div key={pos.driver_id} className='my-position-item'>
                                                    <span className='my-pos-number'>P{pos.position}</span>
                                                    <span className='my-driver-info'>
                                                        {drivers[pos.driver_id]?.code && (
                                                            <img
                                                                src={`/images/drivers/${drivers[pos.driver_id].code}.png`}
                                                                alt={drivers[pos.driver_id].full_name}
                                                                className='my-driver-image-small'
                                                            />
                                                        )}
                                                        <div className='my-driver-text'>
                                                            <span className='my-driver-code'>
                                                                {drivers[pos.driver_id]?.code || pos.driver_id}
                                                            </span>
                                                            <span className='my-driver-full-name'>
                                                                {drivers[pos.driver_id]?.full_name || pos.driver_id}
                                                            </span>
                                                        </div>
                                                    </span>
                                                </div>
                                            ))}
                                    </div>

                                    {prediction.positions.some(p => p.is_dnf) && (
                                        <>
                                            <h4 className='my-dnf-section-title'>DNF:</h4>
                                            <div className='my-positions-grid'>
                                                {prediction.positions
                                                    .filter(p => p.is_dnf)
                                                    .map((pos) => (
                                                        <div key={pos.driver_id} className='my-dnf-position-item my-dnf-item'>
                                                            <span className='my-dnf-pos-number'>DNF</span>
                                                            <span className='my-dnf-driver-info'>
                                                                {drivers[pos.driver_id]?.code && (
                                                                    <img
                                                                        src={`/images/drivers/${drivers[pos.driver_id].code}.png`}
                                                                        alt={drivers[pos.driver_id].full_name}
                                                                        className='my-driver-image-small'
                                                                    />
                                                                )}
                                                                <div className='my-dnf-driver-text'>
                                                                    <span className='my-dnf-driver-code'>
                                                                        {drivers[pos.driver_id]?.code || pos.driver_id}
                                                                    </span>
                                                                    <span className='my-dnf-driver-full-name'>
                                                                        {drivers[pos.driver_id]?.full_name || pos.driver_id}
                                                                    </span>
                                                                </div>
                                                            </span>
                                                        </div>
                                                    ))}
                                            </div>
                                        </>
                                    )}

                                    {prediction.fastest_lap && (
                                        <div className='my-fastest-lap-prediction'>
                                            <span>Fastest Lap: </span>
                                            <strong>
                                                {drivers[prediction.fastest_lap]?.full_name || prediction.fastest_lap}
                                            </strong>
                                        </div>
                                    )}
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
    );
}

export default MyPredictionsPage;
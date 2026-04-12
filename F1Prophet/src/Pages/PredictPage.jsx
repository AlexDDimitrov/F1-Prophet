import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
    DndContext,
    closestCenter,
    KeyboardSensor,
    PointerSensor,
    useSensor,
    useSensors,
} from '@dnd-kit/core';
import {
    arrayMove,
    SortableContext,
    sortableKeyboardCoordinates,
    verticalListSortingStrategy,
} from '@dnd-kit/sortable';
import SortableDriverItem from '../Components/SortableDriverItem';
import './PredictPage.css';

function PredictPage() {
    const navigate = useNavigate();
    const [finishingDrivers, setFinishingDrivers] = useState([]);
    const [dnfDrivers, setDnfDrivers] = useState([]);
    const [fastestLap, setFastestLap] = useState('');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [race, setRace] = useState(null);
    const [timeRemaining, setTimeRemaining] = useState('');

    const sensors = useSensors(
        useSensor(PointerSensor),
        useSensor(KeyboardSensor, {
            coordinateGetter: sortableKeyboardCoordinates,
        })
    );

    useEffect(() => {
        const fetchData = async () => {
            try {
                const driversRes = await fetch('http://localhost:5000/api/drivers');
                if (!driversRes.ok) throw new Error('Failed to fetch drivers');
                const driversData = await driversRes.json();
                
                const sortedDrivers = driversData.sort((a, b) => b.points - a.points);
                
                setFinishingDrivers(sortedDrivers);
                setFastestLap(sortedDrivers[0]?.driver_id || '');
                
                const raceRes = await fetch('http://localhost:5000/api/races/current');
                if (raceRes.ok) {
                    const raceData = await raceRes.json();
                    setRace(raceData);
                }
                
                setLoading(false);
            } catch (err) {
                console.error('Error fetching data:', err);
                setError(err.message);
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    useEffect(() => {
        if (!race?.deadline) return;

        const updateTimer = () => {
            const now = new Date();
            const deadline = new Date(race.deadline);
            const slip = new Date(now.getTime() + (4 * 60 * 60 * 1000));
            const diff = deadline - slip;

            if (diff <= 0) {
                setTimeRemaining('Deadline passed');
                return;
            }
            const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
            const days = Math.floor(diff / (1000 * 60 * 60 * 24));
            const seconds = Math.floor((diff % (1000 * 60)) / 1000);
            setTimeRemaining(`${days}d ${hours}h ${minutes}m ${seconds}s remaining`);
        };

        updateTimer();
        const interval = setInterval(updateTimer, 1000);

        return () => clearInterval(interval);
    }, [race]);

    const handleDragEnd = (event) => {
        const { active, over } = event;

        if (active.id !== over.id) {
            setFinishingDrivers((items) => {
                const oldIndex = items.findIndex((item) => item.driver_id === active.id);
                const newIndex = items.findIndex((item) => item.driver_id === over.id);
                return arrayMove(items, oldIndex, newIndex);
            });
        }
    };

    const handleMoveToDnf = (driverId) => {
        const driver = finishingDrivers.find((d) => d.driver_id === driverId);
        if (driver) {
            setFinishingDrivers((items) => items.filter((d) => d.driver_id !== driverId));
            setDnfDrivers((items) => [...items, driver]);
        }
    };

    const handleMoveToFinishing = (driverId) => {
        const driver = dnfDrivers.find((d) => d.driver_id === driverId);
        if (driver) {
            setDnfDrivers((items) => items.filter((d) => d.driver_id !== driverId));
            setFinishingDrivers((items) => [...items, driver]);
        }
    };

    const handleSubmit = async () => {
        const token = localStorage.getItem('token');
        
        if (!token) {
            alert('Please login to submit predictions');
            navigate('/login');
            return;
        }

        if (!race) {
            alert('No active race found');
            return;
        }

        const prediction = {
            race_id: race.id,
            positions: [
                ...finishingDrivers.map((driver, index) => ({
                    driver_id: driver.driver_id,
                    position: index + 1,
                    is_dnf: false
                })),
                ...dnfDrivers.map((driver) => ({
                    driver_id: driver.driver_id,
                    position: null,
                    is_dnf: true
                }))
            ],
            fastest_lap: fastestLap
        };

        try {
            const response = await fetch('http://localhost:5000/api/predictions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(prediction)
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Failed to submit prediction');
            }

            alert('Prediction submitted successfully!');
        } catch (err) {
            console.error('Error submitting prediction:', err);
            alert(`Error: ${err.message}`);
        }
    };

    if (loading) {
        return (
            <div className='predict-page'>
                <div className='loading'>Loading...</div>
            </div>
        );
    }

    if (error) {
        return (
            <div className='predict-page'>
                <div className='error'>Error: {error}</div>
            </div>
        );
    }

    const allDrivers = [...finishingDrivers, ...dnfDrivers];

    return (
        <div className='predict-page'>
            <button onClick={() => navigate('/')} className='back-button'>
                ← Back to Home
            </button>

            <div className='predict-container'>
                <header className='predict-header'>
                    <h1 className='race-title'>
                        PREDICT: {race?.name || 'Unknown'}
                    </h1>
                    <p className='race-deadline'>
                        Qualifying - Deadline: {timeRemaining || 'N/Ah N/Am remaining'}
                    </p>
                </header>

                <div className='action-buttons'>
                    <button onClick={() => navigate('/my-predictions')} className='view-predictions-btn'>
                        View My Predictions
                    </button>
                </div>

                <div className='predict-content'>
                    <p className='instruction-text'>
                        Drag to reorder • Click × to mark as DNF
                    </p>

                    <div className='drivers-list-container'>
                        <h3 className='section-title'>Finishing Positions</h3>
                        <DndContext
                            sensors={sensors}
                            collisionDetection={closestCenter}
                            onDragEnd={handleDragEnd}
                        >
                            <SortableContext
                                items={finishingDrivers.map((d) => d.driver_id)}
                                strategy={verticalListSortingStrategy}
                            >
                                {finishingDrivers.map((driver, index) => (
                                    <SortableDriverItem
                                        key={driver.driver_id}
                                        driver={driver}
                                        position={index + 1}
                                        onRemove={handleMoveToDnf}
                                        isDnf={false}
                                    />
                                ))}
                            </SortableContext>
                        </DndContext>

                        {dnfDrivers.length > 0 && (
                            <>
                                <h3 className='section-title dnf-title'>DNF</h3>
                                {dnfDrivers.map((driver) => (
                                    <SortableDriverItem
                                        key={driver.driver_id}
                                        driver={driver}
                                        position='DNF'
                                        onRemove={handleMoveToFinishing}
                                        isDnf={true}
                                    />
                                ))}
                            </>
                        )}
                    </div>

                    <div className='fastest-lap-section'>
                        <label htmlFor='fastest-lap'>Fastest Lap Prediction:</label>
                        <select
                            id='fastest-lap'
                            value={fastestLap}
                            onChange={(e) => setFastestLap(e.target.value)}
                            className='fastest-lap-select'
                        >
                            {allDrivers.map((driver) => (
                                <option key={driver.driver_id} value={driver.driver_id}>
                                    {driver.full_name}
                                </option>
                            ))}
                        </select>
                    </div>

                    <button onClick={handleSubmit} className='submit-prediction-btn'>
                        SUBMIT PREDICTION
                    </button>

                    <div className='points-system'>
                        <h3>Points System:</h3>
                        <ul>
                            <li>• Correct position: 10 pts</li>
                            <li>• +1 position: 5 pts</li>
                            <li>• +2 positions: 3 pts</li>
                            <li>• Correct DNF: 5 pts</li>
                            <li>• Correct fastest lap: +5 pts</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default PredictPage;
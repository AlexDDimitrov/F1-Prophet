import React, { useState, useEffect } from 'react'
import DisplayDriver from './driver'
import { driversAPI } from '../services/api'

function CollectDrivers() {
    const [drivers, setDrivers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchDrivers = async () => {
            try {
                const data = await driversAPI.getAllDrivers();
                setDrivers(data);
                setLoading(false);
            } catch (err) {
                setError('Failed to load drivers');
                setLoading(false);
                console.error(err);
            }
        };

        fetchDrivers();
    }, []);

    
    if (loading) {
        return <div className='loading'>Loading drivers...</div>;
    }

    if (error) {
        return <div className='error'>{error}</div>;
    }
    
    return (
        <div className='drivers-grid'>
            {drivers.map((driver) => (
                <DisplayDriver 
                    key={driver.driver_id}
                    name={driver.full_name}
                    team={driver.team}
                    number={driver.number}
                    code={driver.code}
                    nationality={driver.nationality}
                />
            ))}
        </div>
    )
}

export default CollectDrivers
import React, {useState, useEffect} from 'react'
import DisplayDriver from './driver'
import './addDrivers.css'
import F1Loader from '../Components/F1Loader';
import { driversAPI } from '../services/api'

function CollectDrivers({profile}) {
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
        return (
            <div>                
                <div className='predict-page'>
                    <F1Loader message="Loading drivers..."/>
                </div>
            </div>);
    }

    if (error) {
        return <div className='error'>{error}</div>;
    }
    
    return (
        <div className='drivers-grid'>
            {drivers.map((driver) => (
                <DisplayDriver 
                    key={driver.driver_id}
                    driver_id={driver.driver_id}
                    name={driver.full_name}
                    team={driver.team}
                    number={driver.number}
                    code={driver.code}
                    nationality={driver.nationality}
                    position={driver.position}
                    points={driver.points} 
                    favoriteDriver={profile?.favorite_driver}   
                    />
            ))}
        </div>
    )
    /* career_wins = {driver.career_wins}
                    career_podiums = {driver.career_podiums} 
                    career_poles = {driver.career_poles}
                    career_championships = {driver.career_championships} */
}

export default CollectDrivers
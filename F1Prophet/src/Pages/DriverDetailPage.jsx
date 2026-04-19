import React, {useState, useEffect} from "react";
import {useParams, useNavigate} from 'react-router-dom'
import F1Loader from '../Components/F1Loader';
import './DriverDetailPage.css'

function DriverDetailPage() {
    const {driver_id} = useParams();
    const navigate = useNavigate();
    const[driver, setDriver] = useState(null);
    const[loading, setLoading] = useState(true);
    const[error, setError] = useState(null);

    useEffect(() => {
    const fetchDriverDetails = async () => {
        try {
            console.log('Fetching driver with ID:', driver_id);
            
            const response = await fetch(`http://localhost:5000/api/drivers/${driver_id}`);
            
            if (!response.ok) {
                throw new Error('Driver not found');
            }
            
            const data = await response.json();
            console.log('Driver data:', data);
            
            setDriver(data);
            setLoading(false);
        } catch (err) {
            console.error('Error details:', err);
            setError(err.message || 'Failed to load driver details');
            setLoading(false);
        }
    };

    fetchDriverDetails();
}, [driver_id]);

    const getFlagGradient = (nationality) => {
        const flags = {
            'Dutch': 'linear-gradient(180deg, #AE1C28 0%, #AE1C28 33.33%, #FFFFFF 33.33%, #FFFFFF 66.66%, #21468B 66.66%, #21468B 100%)',
            'British': 'linear-gradient(135deg, #012169 0%, #012169 30%, #C8102E 30%, #C8102E 35%, #FFFFFF 35%, #FFFFFF 40%, #012169 40%, #012169 60%, #FFFFFF 60%, #FFFFFF 65%, #C8102E 65%, #C8102E 70%, #012169 70%, #012169 100%)',
            'Spanish': 'linear-gradient(180deg, #AA151B 0%, #AA151B 25%, #F1BF00 25%, #F1BF00 75%, #AA151B 75%, #AA151B 100%)',
            'German': 'linear-gradient(180deg, #000000 0%, #000000 33.33%, #DD0000 33.33%, #DD0000 66.66%, #FFCE00 66.66%, #FFCE00 100%)',
            'French': 'linear-gradient(90deg, #013f79 0%, #044989 33.33%, #FFFFFF 33.33%, #FFFFFF 66.66%, #EF4135 66.66%, #EF4135 100%)',
            'Monegasque': 'linear-gradient(180deg, #CE1126 0%, #CE1126 50%, #FFFFFF 50%, #FFFFFF 100%)',
            'Mexican': 'linear-gradient(90deg, #006847 0%, #006847 33.33%, #FFFFFF 33.33%, #FFFFFF 66.66%, #CE1126 66.66%, #CE1126 100%)',
            'Finnish': `
                linear-gradient(transparent 37%, #003580 37%, #003580 63%, transparent 63%),
                linear-gradient(90deg, transparent 37%, #003580 37%, #003580 50%, transparent 50%),
                linear-gradient(#FFFFFF 0%, #FFFFFF 100%)
            `,
            'Canadian': 'linear-gradient(90deg, #FF0000 0%, #FF0000 25%, #FFFFFF 25%, #FFFFFF 75%, #FF0000 75%, #FF0000 100%)',
            'Australian': 'linear-gradient(135deg, #00247D 0%, #00247D 40%, #012169 40%, #012169 60%, #00247D 60%, #00247D 100%)',
            'Thai': 'linear-gradient(180deg, #A51931 0%, #A51931 16.66%, #FFFFFF 16.66%, #FFFFFF 33.33%, #2D2A4A 33.33%, #2D2A4A 66.66%, #FFFFFF 66.66%, #FFFFFF 83.33%, #A51931 83.33%, #A51931 100%)',
            'Italian': 'linear-gradient(90deg, #009246 0%, #009246 33.33%, #FFFFFF 33.33%, #FFFFFF 66.66%, #CE2B37 66.66%, #CE2B37 100%)',
            'Brazilian': 'linear-gradient(135deg, #009B3A 0%, #009B3A 35%, #FFDF00 35%, #FFDF00 50%, #009B3A 50%, #009B3A 65%, #FFDF00 65%, #009B3A 65%, #009B3A 100%)',
            'Argentine': 'linear-gradient(180deg, #74ACDF 0%, #74ACDF 33.33%, #FFFFFF 33.33%, #FFFFFF 66.66%, #74ACDF 66.66%, #74ACDF 100%)',
            'New Zealander': 'linear-gradient(135deg, #00247D 0%, #00247D 40%, #012169 40%, #012169 60%, #00247D 60%, #00247D 100%)'};
        
        return flags[nationality] || 'linear-gradient(135deg, #1a1a1a 0%, #0a0a0a 100%)';
    };

    const calculateAge = (birthDate) => {
        const today = new Date();
        const birth = new Date(birthDate);

        let age = today.getFullYear() - birth.getFullYear();
        const monthDiff = today.getMonth() - birth.getMonth();
        if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birth.getDate())) {
            age--;
        }
        return age;
    }

    if (loading) {
        return( 
            <div>                
                <div className='predict-page'>
                    <F1Loader message="Loading driver details..." />
                </div>
            </div>);
    }

    if (error || !driver) {
        return (
            <div className='error-page'>
                <h2>{error || 'Driver not found'}</h2>
                <button onClick={() => navigate('/drivers')} className='back-btn'>
                    ← Back to Drivers
                </button>
            </div>
        );
    }

    const driverImage = `/images/drivers/${driver.code}.png`;

    return(
        <div className="driver-detail-page">
            <button onClick={() => navigate('/drivers')} className='back-button'>
                ← Back to Drivers
            </button>

            <section className="hero-driver-banner">
                <div
                    className="hero-driver-background"
                    style={{background: getFlagGradient(driver.nationality)}}
                ></div>

                <div className='hero-driver-content'>
                    <div className='hero-driver-image'>
                        <img 
                            src={driverImage} 
                            alt={driver.full_name}
                            onError={(e) => {
                                e.target.style.display = 'none';
                                e.target.nextSibling.style.display = 'flex';
                            }}
                        />
                        <div className='hero-driver-placeholder' style={{display: 'none'}}>
                            <span>{driver.code}</span>
                        </div>
                    </div>
                    
                    <div className="hero-driver-info">
                        <h1 className="driver-name">{driver.full_name}</h1>
                        <div className='driver-meta'>
                            <span className='meta-item'>#{driver.number}</span>
                            <span className='meta-divider'>•</span>
                            <span className='meta-item'>{driver.nationality}</span>
                            <span className='meta-divider'>•</span>
                            <span className='meta-item'>{driver.team}</span>
                        </div>
                    </div>
                </div>
            </section>

            <section className="stats-section">
                <div className="stat-card">
                    <h3 className="card-title">2026 SEASON</h3>
                    <div className="card-content">
                        <div className="stat-item">
                            <span className="stat-label">Position</span>
                            <span className='stat-value'>{driver.position ? `P${driver.position}` : 'N/A'}</span>
                        </div>
                        <div className='stat-item'>
                            <span className='stat-label'>Points</span>
                            <span className='stat-value'>{driver.points || 0}</span>
                        </div>
                        <div className='stat-item'>
                            <span className='stat-label'>Wins</span>
                            <span className='stat-value'>{driver.wins || 0}</span>
                        </div>
                    </div>
                </div>

                <div className="stat-card">
                    <h3 className='card-title'>CAREER STATS</h3>
                    <div className='card-content'>
                        <div className='stat-item'>
                            <span className='stat-label'>World Championships</span>
                            <span className='stat-value'>{driver.career_championships || 0}</span>
                        </div>
                        <div className='stat-item'>
                            <span className='stat-label'>Wins</span>
                            <span className='stat-value'>{driver.career_wins || '0'}</span>
                        </div>
                        <div className='stat-item'>
                            <span className='stat-label'>Podiums</span>
                            <span className='stat-value'>{driver.career_podiums || '0'}</span>
                        </div>
                        <div className='stat-item'>
                            <span className='stat-label'>Poles</span>
                            <span className='stat-value'>{driver.career_poles || '0'}</span>
                        </div>
                    </div>
                </div>
            </section>

            <section className='biography-section'>
                <h2 className='section-title'>BIOGRAPHY</h2>
                <div className='bio-content'>
                    <div className='bio-details'>
                        <div className='bio-item'>
                            <span className='bio-label'>Born:</span>
                            <span className='bio-value'>
                                {new Date(driver.date_of_birth).toLocaleDateString('en-US', { 
                                    year: 'numeric', 
                                    month: 'long', 
                                    day: 'numeric' 
                                })} (Age: {calculateAge(driver.date_of_birth)})
                            </span>
                        </div>
                        <div className='bio-item'>
                            <span className='bio-label'>Nationality:</span>
                            <span className='bio-value'>{driver.nationality}</span>
                        </div>
                        <div className='bio-item'>
                            <span className='bio-label'>Team:</span>
                            <span className='bio-value'>{driver.team}</span>
                        </div>
                        <div className='bio-item'>
                            <span className='bio-label'>Number:</span>
                            <span className='bio-value'>#{driver.number}</span>
                        </div>
                    </div>
                </div>
            </section>

        </div>
    )
}

export default DriverDetailPage

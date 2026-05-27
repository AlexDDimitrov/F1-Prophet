import React from 'react'
import {useNavigate} from 'react-router-dom'
import './driver.css'

function DisplayDriver({ 
    driver_id,
    name, 
    team, 
    number, 
    code, 
    nationality, 
    position, 
    points 
}) {
    const navigate = useNavigate();

    const handleViewProfile = () => {
        navigate(`/drivers/${driver_id}`);
    };
    const driverImage = `/images/drivers/${code}.png`;
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
    
    return (
        <div className='driver-card'>
            <div 
                className='card-background' 
                style={{ background: getFlagGradient(nationality) }}
            ></div>
            <div className='driver-image-section'>
                <img 
                    src={driverImage} 
                    alt={name}
                    className='driver-image'
                    onError={(e) => {
                        e.target.style.display = 'none';
                        e.target.nextSibling.style.display = 'flex';
                    }}
                />
                <div className='driver-placeholder' style={{display: 'none'}}>
                    <span className='placeholder-code'>{code}</span>
                </div>
            </div>
            <div className='driver-info-boxes'>
                <div className='driver-info-box'>
                    <span className='driver-info-label'>NAME</span>
                    <span className='driver-info-value'>{name}</span>
                </div>
                
                <div className='driver-info-box'>
                    <span className='driver-info-label'>TEAM</span>
                    <span className='driver-info-value'>{team}</span>
                </div>
                
                <div className='driver-info-box'>
                    <span className='driver-info-label'>NUMBER</span>
                    <span className='driver-info-value'>{number}</span>
                </div>

                <div className='driver-info-box'>
                    <span className='driver-info-label'>NATIONALITY</span>
                    <span className='driver-info-value'>{nationality}</span>
                </div>
                
                <div className='driver-info-box'>
                    <span className='driver-info-label'>POSITION</span>
                    <span className='driver-info-value'>
                        {position ? `P${position}` : 'DNF'}
                    </span>
                </div>
                
                <div className='driver-info-box'>
                    <span className='driver-info-label'>POINTS</span>
                    <span className='driver-info-value'>{points || 0}</span>
                </div>
                
                <button className='view-profile-btn' onClick={handleViewProfile}>
                    View Profile →
                </button>
            </div>
        </div>
    )
}

export default DisplayDriver
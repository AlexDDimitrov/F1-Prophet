import React from 'react';
import './team.css';

function Team({ team }) {
    const teamImage = `/images/teams/${team.team_id}.png`;

    return (
        <div className='team-card'>
            <div className='team-image-section'>
                <img 
                    src={teamImage} 
                    alt={team.name}
                    className='team-image'
                    onError={(e) => {
                        e.target.style.display = 'none';
                        e.target.nextSibling.style.display = 'flex';
                    }}
                />
                <div className='team-placeholder' style={{display: 'none'}}>
                    <span className='placeholder-name'>{team.name}</span>
                </div>
            </div>

            <div className='team-info-boxes'>
                <div className='info-box'>
                    <span className='info-label'>Name</span>
                    <span className='info-value'>{team.name}</span>
                </div>

                <div className='info-box'>
                    <span className='info-label'>Nationality</span>
                    <span className='info-value'>{team.nationality}</span>
                </div>

                <div className='info-box'>
                    <span className='info-label'>Position</span>
                    <span className='info-value'>
                        {team.position ? `P${team.position}` : 'N/A'}
                    </span>
                </div>

                <div className='info-box'>
                    <span className='info-label'>Points</span>
                    <span className='info-value'>{team.points}</span>
                </div>
            </div>
        </div>
    )
}

export default Team;
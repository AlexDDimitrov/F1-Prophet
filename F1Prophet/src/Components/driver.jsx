import React from 'react'
import './driver.css'

function DisplayDriver({name, 
    team, 
    number, 
    code, 
    nationality, 
    career_wins, 
    career_podiums, 
    career_poles, 
    career_championships}) {
    return (
        <div className='driver-card'>            
            <h2 className='driver-name'>{name}</h2>
            
        <div className='driver-photo'>
                <div className='photo-placeholder'>{code || 'pic'}</div>
        </div>

            <div className='driver-info'>
                <span className='driver-team'>{team}</span>
                <span className='driver-number'>#{number}</span>
            </div>
            <div className='driver-stats'>
                <div className='stat'>
                    <span className='stat-label'>Titles</span>
                    <span className='stat-value'>{career_championships || 0}</span>
                </div>
                <div className='stat'>
                    <span className='stat-label'>Wins</span>
                    <span className='stat-value'>{career_wins || 0}</span>
                </div>
                <div className='stat'>
                    <span className='stat-label'>Podiums</span>
                    <span className='stat-value'>{career_podiums || 0}</span>
                </div>
                <div className='stat'>
                    <span className='stat-label'>Poles</span>
                    <span className='stat-value'>{career_poles || 0}</span>
                </div>
            </div>
            
            <div className='driver-nationality'>
                {nationality}
            </div>
        </div>
    )
}

export default DisplayDriver
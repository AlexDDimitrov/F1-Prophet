import React from 'react'
import './driver.css'

function DisplayDriver({name}) {
    return (
        <div className='driver-card'>
            <div className='driver-photo'>
                <div className='photo-placeholder'>Photo</div>
            </div>
            <h2 className='driver-name'>{name}</h2>
            <div className='driver-info'>
                <span className='driver-team'>Team Name</span>
                <span className='driver-number'>Number</span>
            </div>
        </div>
    )
}

export default DisplayDriver
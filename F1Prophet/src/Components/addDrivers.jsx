import React from 'react'
import DisplayDriver from './driver'

function CollectDrivers() {
    return (
        <div>
            <DisplayDriver name="Max Verstappen" />
            <DisplayDriver name="Charles Leclerc" />
            <DisplayDriver name="Lando Norris" />
            <DisplayDriver name="Lewis Hamilton" />
            <DisplayDriver name="Carlos Sainz" />
            <DisplayDriver name="Oscar Piastri" />
            <DisplayDriver name="George Russell" />
            <DisplayDriver name="Sergio Perez" />
        </div>
    )
}

export default CollectDrivers
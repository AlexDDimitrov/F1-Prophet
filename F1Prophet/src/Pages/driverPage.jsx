import CollectDrivers from '../Components/addDrivers'
import React from 'react'
import './DriverPage.css'
import './HomePage.css'

function DriverPage() {
    return (
        <div>
            <div className='driver-page'>
                <header className='driver-header'>
                    <h1 className='page-title'>F1 Drivers 2026</h1>
                    <p className='page-subtitle'>Meet the 2026 grid pilots</p>
                </header>

                <section className='drivers-section'>
                    <CollectDrivers/>
                </section>
            </div>
        </div>
    )
}

export default DriverPage
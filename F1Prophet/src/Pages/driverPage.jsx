import CollectDrivers from '../Components/addDrivers'
import React from 'react'
import {useNavigate} from 'react-router-dom'
import './DriverPage.css'
import './HomePage.css'

function DriverPage() {
        
    const navigate = useNavigate();
    return (
        <div>

            <button onClick={() => navigate('/')} className='back-button'>
                ← Back to Home Page
            </button>

            <div className='driver-page'>
                <header className='driver-header'>
                    <h1 className='page-title'>F1 Drivers 2026</h1>
                    <p className='page-subtitle'>Meet the 2026 grid pilots</p>
                </header>

                <section className='drivers-section'>
                    <CollectDrivers/>
                </section>
            </div>

            <p className='image-credit'>
                Pictures from https://www.formulaonehistory.com/
            </p>
        </div>
    )
}

export default DriverPage
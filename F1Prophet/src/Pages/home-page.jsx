import React from 'react'
import { Link } from 'react-router-dom'
import './HomePage.css'

function HomePage() {
    return (
        <div className='homepage'>
            <section className='hero'>
                <div className='hero-content'>
                    <h1 className='hero-title'>
                        <span className='title-line1'>F1 Prophet</span>
                        <span className='title-line2'>Race and Win</span>
                    </h1>
                    <p className='hero-subtitle'>
                        Predict results before qualifying and score points.
                        
                    </p>
                    <div className='hero-buttons'>
                        <Link to='/' className='btn btn-primary'>
                            Register
                        </Link>
                        <Link to='/' className='btn btn-primary'>
                            Login
                        </Link>
                        <Link to='/' className='btn btn-primary'>
                            Predict
                        </Link>
                        <Link to='/drivers' className='btn btn-primary'>
                            View Drivers
                        </Link>
                    </div>
                </div>
            </section>
        </div>
    )
}

//buttons for login, register, predict, drivers to be done


export default HomePage
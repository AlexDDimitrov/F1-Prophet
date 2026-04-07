import React from 'react'
import {Link} from 'react-router-dom'
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
                        Predict results before qualifying and score points. {<br></br>}
                        {localStorage.getItem('user') && (
                            <span>Welcome back, {JSON.parse(localStorage.getItem('user')).username}!</span>
                        )}
                    </p>
                    <div className='hero-buttons'>
                        <Link to='/register' className='btn btn-primary'>
                            Register
                        </Link>
                        <Link to='/login' className='btn btn-primary'>
                            Login
                        </Link>
                        <Link to='/' onClick={() => {
                            localStorage.removeItem('user');
                            localStorage.removeItem('token');
                            window.location.reload();
                        }} refresh={true} className='btn btn-primary'>
                            Log out
                        </Link>
                        <Link to='/' className='btn btn-primary'>
                            Predict
                        </Link>
                        <Link to='/drivers' className='btn btn-primary'>
                            View Drivers
                        </Link>
                        <Link to='/teams' className='btn btn-primary'>
                            View Teams
                        </Link>
                    </div>
                </div>

                <div className='video-section'>
                    <div className='video-wrapper'>
                        <video autoPlay muted loop playsInline>
                            <source src="/videos/New 2026 F1 Opening Titles - FORMULA 1 (1080p, h264).mp4" type="video/mp4" />
                        </video>
                    </div>
                    <p className='video-credit'>
                        Video from https://www.youtube.com/watch?v=Sks_fMr2Yss
                    </p>
                </div>

            </section>
        </div>
    )
}

export default HomePage
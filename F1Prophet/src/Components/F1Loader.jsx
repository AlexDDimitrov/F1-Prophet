import React from 'react';
import './F1Loader.css';

function F1Loader({ track = 'suzuka', message = 'Loading...' }) {
    const tracks = {
        /*monza: (
            <svg viewBox="0 0 200 200" className="track-svg">
                <path
                    className="track-path"
                    d="M 30,100 L 30,50 Q 30,30 50,30 L 150,30 Q 170,30 170,50 L 170,150 Q 170,170 150,170 L 50,170 Q 30,170 30,150 Z"
                    fill="none"
                    stroke="#333"
                    strokeWidth="15"
                />
                <circle className="racing-dot" r="5" fill="#ED1C01">
                    <animateMotion
                        dur="3s"
                        repeatCount="indefinite"
                        path="M 30,100 L 30,50 Q 30,30 50,30 L 150,30 Q 170,30 170,50 L 170,150 Q 170,170 150,170 L 50,170 Q 30,170 30,150 Z"
                    />
                </circle>
            </svg>
        ),*/
        
        suzuka: (
            <div className='video-wrapper-loading'>
                <video className='loader-vid' autoPlay muted loop playsInline>
                    <source src="/videos/F1ProphetLoaderShort.mov" type="video/mp4" />
                </video>
            </div>
        )
    };

    return (
        <div className="f1-loader">
            <div className="loader-content-vid">
                <p className="loader-message-vid">{message}</p>
                {tracks[track] || tracks.suzuka}
            </div>
        </div>
    );
}

export default F1Loader;
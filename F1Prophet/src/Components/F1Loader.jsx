import React, {useState} from 'react';
import './F1Loader.css';

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

const TRACK_DATA = {
    suzuka: (
        <div className='video-wrapper-loading'>
            <video className='loader-vid' autoPlay muted loop playsInline>
                <source src="/videos/F1ProphetLoaderShort.webm" type="video/webm" />
            </video>
        </div>
    ),
    albert_park: (
        <div className='video-wrapper-loading'>
            <video className='loader-vid' autoPlay muted loop playsInline>
                <source src="/videos/F1ProphetLoaderShort2.webm" type="video/webm" />
            </video>
        </div>
    ),
    spa: (
    <div className="video-wrapper-loading">
      <video className="loader-vid" autoPlay muted loop playsInline>
        <source src="/videos/F1LoaderProphetShort3.webm" type="video/webm" />
      </video>
    </div>
    ),
    hungary: (
    <div className="video-wrapper-loading">
      <video className="loader-vid" autoPlay muted loop playsInline>
        <source src="/videos/F1LoaderProphetShort4.webm" type="video/webm" />
      </video>
    </div>
    ),
    china: (
    <div className="video-wrapper-loading">
      <video className="loader-vid" autoPlay muted loop playsInline>
        <source src="/videos/F1LoaderProphetShort5.webm" type="video/webm" />
      </video>
    </div>
    ),
    barcelona: (
    <div className="video-wrapper-loading">
      <video className="loader-vid" autoPlay muted loop playsInline>
        <source src="/videos/F1LoaderProphetShort6.webm" type="video/webm" />
      </video>
    </div>
    ),
    canada: (
    <div className="video-wrapper-loading">
      <video className="loader-vid" autoPlay muted loop playsInline>
        <source src="/videos/F1LoaderProphetShort7.webm" type="video/webm" />
      </video>
    </div>
    ),
    miami: (
    <div className="video-wrapper-loading">
      <video className="loader-vid" autoPlay muted loop playsInline>
        <source src="/videos/F1LoaderProphetShort8.webm" type="video/webm" />
      </video>
    </div>
    ),
    monaco: (
    <div className="video-wrapper-loading">
      <video className="loader-vid" autoPlay muted loop playsInline>
        <source src="/videos/F1LoaderProphetShort9.webm" type="video/webm" />
      </video>
    </div>
    ),
    silverstone: (
    <div className="video-wrapper-loading">
      <video className="loader-vid" autoPlay muted loop playsInline>
        <source src="/videos/F1LoaderProphetShort10.webm" type="video/webm" />
      </video>
    </div>
    ),
    spielberg: (
    <div className="video-wrapper-loading">
      <video className="loader-vid" autoPlay muted loop playsInline>
        <source src="/videos/F1LoaderProphetShort11.webm" type="video/webm" />
      </video>
    </div>
    ),
    zandvoort: (
    <div className="video-wrapper-loading">
      <video className="loader-vid" autoPlay muted loop playsInline>
        <source src="/videos/F1LoaderProphetShort12.webm" type="video/webm" />
      </video>
    </div>
    ),
};

function F1Loader({message = 'Loading...'}) {
    const [selectedTrack] = useState(() => {
        const keys = Object.keys(TRACK_DATA);
        const randomIndex = Math.floor(Math.random() * keys.length);
        return TRACK_DATA[keys[randomIndex]];
    });

    return (
        <div className="f1-loader">
            <div className="loader-content-vid">
                <p className="loader-message-vid">{message}</p>
                {selectedTrack}
            </div>
        </div>
    );
}

export default F1Loader;
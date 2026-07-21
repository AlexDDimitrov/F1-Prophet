import React, { useState } from 'react';
import './F1Loader.css';

const TRACK_DATA = {
  suzuka: (
    <div className="video-wrapper-loading">
      <video className="loader-vid" autoPlay muted loop playsInline>
        <source src="/videos/F1ProphetLoaderShort.webm" type="video/webm" />
      </video>
    </div>
  ),
  albert_park: (
    <div className="video-wrapper-loading">
      <video className="loader-vid" autoPlay muted loop playsInline>
        <source src="/videos/F1ProphetLoaderShort2.webm" type="video/webm" />
      </video>
    </div>
  ),
  spa: (
    <div className="video-wrapper-loading">
      <video className="loader-vid" autoPlay muted loop playsInline>
        <source src="/videos/F1ProphetLoaderShort3.webm" type="video/webm" />
      </video>
    </div>
  ),
};

function F1Loader({ message = "Loading..." }) {
  const [selectedTrackKey] = useState(() => {
    const keys = Object.keys(TRACK_DATA);
    const randomIndex = Math.floor(Math.random() * keys.length);
    return keys[randomIndex];
  });

  return (
    <div className="f1-loader">
      <div className="loader-content-vid">
        <p className="loader-message-vid">{message}</p>
        {TRACK_DATA[selectedTrackKey]}
      </div>
    </div>
  );
}

export default F1Loader;
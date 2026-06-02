import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import CollectDrivers from '../Components/addDrivers';
import './DriverPage.css';
import './HomePage.css';
import F1Loader from '../Components/F1Loader';

function DriverPage() {
    const navigate = useNavigate();
    const [profile, setProfile] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadProfile = async () => {
            const token = localStorage.getItem('token');
            if (!token) {
                setLoading(false);
                return;
            }

            try {
                const res = await fetch('http://localhost:5000/api/users/profile', {
                    headers: { Authorization: `Bearer ${token}` }
                });

                if (res.ok) {
                    const data = await res.json();
                    setProfile(data);
                }
                setLoading(false);
            } catch (err) {
                console.error("Error loading profile:", err);
                setLoading(false);
            } finally {
                setLoading(false);
            }
        };

        loadProfile();
    }, []);

    useEffect(() => {
        window.myProfile = profile;
        //console.log("PROFILE FROM BACKEND:", profile);
    }, [profile]);

    if (loading) {
        return (
            <div className="predict-page">
                <F1Loader message="loading driver data..." />
            </div>
        );
    }

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
                    <CollectDrivers profile={profile} />
                </section>
            </div>

            <p className='image-credit'>
                Pictures from https://www.formulaonehistory.com/
            </p>
        </div>
    );
}

export default DriverPage;
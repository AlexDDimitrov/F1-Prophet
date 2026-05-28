import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import CollectTeams from '../Components/addTeams';
import './TeamPage.css';
import F1Loader from '../Components/F1Loader';

function TeamPage() {
    const navigate = useNavigate();
    const [profile, setProfile] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadProfile = async () => {
            const token = localStorage.getItem('token');
            if (!token) return;

            try {
                const res = await fetch('http://localhost:5000/api/users/profile', {
                    headers: { Authorization: `Bearer ${token}` }
                });

                if (res.ok) {
                    const data = await res.json();
                    setProfile(data);
                }
            } catch (err) {
                console.error("Error loading profile:", err);
            } finally {
                setLoading(false);
            }
        };

        loadProfile();
    }, []);

    if (loading) {
        return (
            <div className="predict-page">
                <F1Loader message="Loading profile..." />
            </div>
        );
    }

    return (
        <div>
            <button onClick={() => navigate('/')} className='back-button'>
                ← Back to Home Page
            </button>

            <div className='team-page'>
                <header className='team-header'>
                    <h1 className='page-title'>F1 Teams 2026</h1>
                    <p className='page-subtitle'>Meet the 2026 constructors</p>
                </header>

                <section className='teams-section'>
                    <CollectTeams profile={profile} />
                </section>
            </div>

            <p className='image-credit'>
                Pictures from https://www.formula1.com/
            </p>
        </div>
    );
}

export default TeamPage;
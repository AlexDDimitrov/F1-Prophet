import React from 'react';
import {useNavigate} from 'react-router-dom';
import CollectTeams from '../Components/addTeams';
import './TeamPage.css';

function TeamPage() {
    const navigate = useNavigate();

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
                    <CollectTeams />
                </section>
            </div>

            <p className='image-credit'>
                Pictures from https://www.formula1.com/
            </p>
        </div>
    );
}

export default TeamPage;